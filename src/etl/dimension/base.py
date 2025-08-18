import pandas as _pd

from sqlalchemy import text as _text
from datetime import datetime as _dt
from pytz import timezone as _timezone
from pathlib import Path as _Path

from src.connection.postgresql import PostgreSQL as _PostgreSQL
from src.etl.utils.types import (
    df_header as _df_header,
    dtypes_columns as _dtypes_columns
)


class Base:
    DEFAULT_PATH: _Path = _Path('./source/dim')

    TABLE_NAME: str

    def __init__(
        self,
        conn_output: _PostgreSQL,
        columns_pk: list[str],
        column_sk: str,
        schema: str = 'dw',
        parquet: bool = False,
    ) -> None:
        self.conn_output = conn_output
        self.table_name = self.__class__.TABLE_NAME
        self.columns_pk = columns_pk
        self.schema = schema
        self.column_sk = column_sk
        self.parquet = parquet

        self.df_load: _pd.DataFrame
        self.dimension: _pd.DataFrame
        self.dt_update = _dt.now(_timezone('America/Sao_Paulo'))

    def extract_dimension(self):
        sql = f'--sql SELECT {",".join(self.columns_pk)} FROM {self.schema}.{self.table_name} ;'[5:-1]
        self.df_dimension = _pd.read_sql_query(sql, con=self._conn_output)

    def extract(self):
        raise NotImplementedError

    def treat(self):
        raise NotImplementedError

    def dtypes(self):
        dtypes = _dtypes_columns(self._conn_output, self.table_name, self.schema)
        print(dtypes)
        dtype = {k : v for k, v in dtypes.items() if k in self.df_dimension.columns}
        self.df_dimension = self.df_dimension.astype(dtype)

        dtype = {k : v for k, v in dtypes.items() if k in self.df_load.columns}
        self.df_load = self.df_load.astype(dtype)

    def set_sk(self):
        if self.df_load.empty:
            raise NotImplementedError

        sql = f'''--sql 
            SELECT COALESCE(MAX({self.column_sk}), 1)
            FROM {self.schema}.{self.table_name}
        ;'''[5:-1]

        with self._conn_output.connect() as conn: 
            _max = (conn.execute(_text(sql)).fetchone() or [1])[0]

        self.df_load[self.column_sk] = range(_max, _max + len(self.df_load))

        if _max == 1:
            self.df_load = _pd.concat([
                self.df_load,
                _df_header(self._conn_output, self.table_name, self.schema)]
            )

    def set_dt(self):
        self.df_load['dt_atualizacao'] = self.dt_update

    def load(self):
        df = self.df_load.merge(
            self.df_dimension,
            on=self.columns_pk,
            how='left',
            indicator=True
        )

        df = df[df['_merge'] == 'left_only'].drop('_merge', axis=1)

        df.to_sql(
            self.table_name,
            self._conn_output,
            index=False,
            schema=self.schema,
            if_exists='append',
        )

    def before_run(self):
        self._conn_output = self.conn_output.connect()

    @classmethod
    def path(cls):
        return cls.DEFAULT_PATH / f'{cls.TABLE_NAME}.parquet'

    def to_parquet(self):
        sql = f'--sql SELECT {",".join(self.columns_pk + [self.column_sk])} FROM {self.schema}.{self.table_name} ;'[5:-1]
        self.df_dimension = _pd.read_sql_query(sql, con=self._conn_output)
        self.df_dimension.astype('string').to_parquet(self.path(), index=False)

    @classmethod
    def join(cls, as_origin: str, as_dimension: str, *args, **kwargs) -> str:
        raise NotImplementedError

    def run(self):
        self.before_run()
        self.extract()
        self.extract_dimension()
        if not self.df_load.empty:
            self.treat()
            self.dtypes()
            self.set_sk()
            self.set_dt()
            self.load()

        if self.parquet:
            self.to_parquet()
