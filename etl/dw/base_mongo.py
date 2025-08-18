import pandas as _pd

from pathlib import Path as _Path

from src.etl.dimension.base import Base as _Base
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class Column:
    def __init__(self, name_origin: str, name_dimesion: str) -> None:
        self.name_origin = name_origin
        self.name_dimesion = name_dimesion


class BaseMongo(_Base):
    DEFAULT_PATH: _Path = _Path('./source/dim')

    TABLE_NAME: str

    def __init__(
        self,
        conn_input: _MongoDB,
        conn_output: _PostgreSQL,
        table_origin: str,
        columns: list[Column],
        columns_pk: list[str],
        column_sk: str,
        schema: str = 'dw',
        database: str = 'stage',
        chunksize: int = 40000,
        parquet: bool = False,
    ) -> None:
        self.conn_input = conn_input
        self.table_name = self.__class__.TABLE_NAME
        self.table_origin = table_origin
        self.columns = columns
        self.database = database
        self.chunksize = chunksize

        self.df_extract: _pd.DataFrame

        super().__init__(conn_output, columns_pk, column_sk, schema, parquet)

    def extract(self):
        colletion = self._conn_input[self.database][self.table_origin]

        pipeline = [
            {
                '$match': {
                    c.name_origin: {"$ne": None}
                    for c in self.columns
                    if c.name_dimesion in self.columns_pk
                },
            },
            {
                '$match': {
                    c.name_origin: {"$ne": ""}
                    for c in self.columns
                    if c.name_dimesion in self.columns_pk
                }
            },
            {
                '$group': {
                    '_id': {
                        c.name_dimesion: f'${c.name_origin}'
                        for c in self.columns
                    }
                }
            },
            {
                '$project': {
                    '_id': 0
                } | {
                    c.name_dimesion: f'$_id.{c.name_dimesion}'
                    for c in self.columns
                }
            },
        ]

        self.cursor = colletion.aggregate(pipeline)

    def before_run(self):
        super().before_run()
        self._conn_input = self.conn_input.connect()

    def itercursor(self):
        _list = []
        i = 0
        for i, c in enumerate(self.cursor, 1):
            _list.extend([c])
            if i % self.chunksize == 0:
                yield _pd.DataFrame(_list)
                _list = []

        yield _pd.DataFrame(_list)

    def run(self):
        self.before_run()
        self.extract()
        self.extract_dimension()
        for self.df_extract in self.itercursor():
            if not self.df_extract.empty:
                self.treat()
                self.dtypes()
                self.set_sk()
                self.set_dt()
                self.load()

        if self.parquet:
            self.to_parquet()


class TemplateBaseMongo(BaseMongo):
    def __init__(self, conn_output: _PostgreSQL, conn_input: _MongoDB | None = None) -> None:
        raise