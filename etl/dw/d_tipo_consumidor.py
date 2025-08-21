from typing_extensions import override as _override

from etl.dw.base_mongo import (
    BaseMongo as _BaseMongo,
    Column as _Column
)
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionTipoConsumidor(_BaseMongo):
    TABLE_NAME = 'd_tipo_consumidor'

    def __init__(self, conn_input: _MongoDB, conn_output: _PostgreSQL):
        columns = [
            _Column('DscClasseConsumo', 'no_classe_consumo'),
            _Column('SigTipoConsumidor', 'cd_tipo_consumidor'),
        ]

        super().__init__(
            conn_input,
            conn_output,
            table_origin='stg_aneel_empreendimento_geracao_distribuida',
            columns=columns,
            columns_pk=['no_classe_consumo', 'cd_tipo_consumidor'],
            column_sk='sk_tipo_consumidor',
            parquet=True,
        )

    def treat(self):
        no_tipo_consumidor = {
            "PF": "PESSOA FÍSICA",
            "PJ": "PESSOA JURÍDICA",
        }

        self.df_load = self.df_extract.assign(
            no_classe_consumo=lambda x: x.no_classe_consumo.str.upper(),
            no_tipo_consumidor=lambda x: x.cd_tipo_consumidor.apply(no_tipo_consumidor.get)
        )

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str = 'tc',
        no_classe_consumo_origin: str = 'no_classe_consumo',
        cd_cd_tipo_consumidor_origin: str = 'cd_tipo_consumidor',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.no_classe_consumo = {as_origin}.{no_classe_consumo_origin}
                AND {as_dimension}.cd_tipo_consumidor = {as_origin}.{cd_cd_tipo_consumidor_origin}
        ;"""[5:-1]

        return sql
