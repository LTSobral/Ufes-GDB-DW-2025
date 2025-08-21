import pandas as _pd

from typing_extensions import override as _override

from src.etl.dimension.base import Base as _Base
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionCompetencia(_Base):
    TABLE_NAME = 'd_competencia'

    def __init__(self, conn_output: _PostgreSQL, conn_input=None):
        super().__init__(
            conn_output,
            columns_pk=['nu_competencia'],
            column_sk='sk_competencia',
            parquet=True,
        )

    def extract(self):
        data_inicio = '2000-01-01'
        data_fim = (_pd.to_datetime('today') + _pd.DateOffset(years=1)).strftime('%Y-%m-%d')

        datas_mensais = _pd.date_range(start=data_inicio, end=data_fim, freq='MS')

        self.df_extract = _pd.DataFrame(datas_mensais, columns=['dt_referencia'])

        
        self.df_extract['nu_ano'] = self.df_extract['dt_referencia'].dt.year
        self.df_extract['nu_mes'] = self.df_extract['dt_referencia'].dt.month

        meses_map = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        self.df_extract['no_mes'] = self.df_extract['nu_mes'].map(meses_map)

        self.df_extract['nu_competencia'] = self.df_extract['dt_referencia'].dt.strftime('%Y%m').astype(int)
        
        self.df_extract['dt_inicio_mes'] = self.df_extract['dt_referencia']

        self.df_extract['dt_fim_mes'] = self.df_extract['dt_referencia'] + _pd.offsets.MonthEnd(1)

        self.df_load = self.df_extract


    def run(self):
        self.before_run()
        self.extract()
        self.extract_dimension()
        self.set_sk()
        self.set_dt()

        self.load()

        if self.parquet:
            self.to_parquet()

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str='dat',
        nu_competencia_origin: str='nu_competencia',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.nu_competencia = {as_origin}.{nu_competencia_origin}
        ;"""[5:-1]

        return sql