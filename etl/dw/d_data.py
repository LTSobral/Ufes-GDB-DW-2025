import pandas as _pd

from typing_extensions import override as _override

from src.etl.dimension.base import Base as _Base
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionData(_Base):
    TABLE_NAME = 'd_data'

    def __init__(self, conn_output: _PostgreSQL):
        super().__init__(
            conn_output,
            columns_pk=['dt_completa'],
            column_sk='sk_data',
            parquet=True,
        )

    def extract(self):
        data_inicio = '2000-01-01'
        datas = _pd.to_datetime(_pd.date_range(start=data_inicio, periods=7))

        mapa_mes = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

        dados = {
            'nu_dia': datas.day,
            'nu_mes': datas.month,
            'no_mes': datas.month.map(mapa_mes),
            'nu_ano': datas.year,
            'dt_completa': datas.date
        }

        self.df_load = _pd.DataFrame(dados)


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
        dt_completa_origin: str='dt_completa',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.dt_completa = {as_origin}.{dt_completa_origin}
        ;"""[5:-1]

        return sql