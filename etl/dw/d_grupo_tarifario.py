from typing_extensions import override as _override

from etl.dw.base_mongo import (
    BaseMongo as _BaseMongo,
    Column as _Column
)
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionGrupoTarifario(_BaseMongo):
    TABLE_NAME = 'd_grupo_tarifario'

    def __init__(self, conn_input: _MongoDB, conn_output: _PostgreSQL):
        columns = [
            _Column('DscSubGrupoTarifario', 'cd_grupo_tarifario'),
        ]

        super().__init__(
            conn_input,
            conn_output,
            table_origin='stg_aneel_empreendimento_geracao_distribuida',
            columns=columns,
            columns_pk=['cd_grupo_tarifario'],
            column_sk='sk_grupo_tarifario',
            parquet=True,
        )

    def treat(self):
        ds_grupo_tarifario = {
            "A1": "TENSÃO DE FORNECIMENTO IGUAL OU SUPERIOR A 230 KV",
            "A2": "TENSÃO DE FORNECIMENTO DE 88 KV A 138 KV",
            "A3": "TENSÃO DE FORNECIMENTO DE 69 KV",
            "A3A": "TENSÃO DE FORNECIMENTO DE 30 KV A 44 KV",
            "A4": "TENSÃO DE FORNECIMENTO DE 2,3 KV A 25 KV",
            "AS": "SUBTERRÂNEO",
            "B1": "RESIDENCIAL",
            "B2": "RURAL",
            "B3": "DEMAIS CLASSES",
            "B4": "ILUMINAÇÃO PÚBLICA",
        }

        self.df_load = self.df_extract.assign(
            ds_grupo_tarifario=lambda x: x.cd_grupo_tarifario.apply(
                ds_grupo_tarifario.get)
        )

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str = 'gc',
        cd_grupo_tarifario_origin: str = 'cd_grupo_tarifario',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.cd_grupo_tarifario = {as_origin}.{cd_grupo_tarifario_origin}
        ;"""[5:-1]

        return sql
