import re as _re

from typing_extensions import override as _override

from etl.dw.base_mongo import (
    BaseMongo as _BaseMongo,
    Column as _Column
)
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionEmpresaDistribuidora(_BaseMongo):
    TABLE_NAME = 'd_empresa_distribuidora'

    def __init__(self, conn_input: _MongoDB, conn_output: _PostgreSQL):
        columns = [
            _Column('SigAgente', 'cd_empresa_distribuidora'),
            _Column('NomAgente', 'no_empresa_distribuidora'),
            _Column('NumCNPJDistribuidora', 'no_cnpj'),
        ]

        super().__init__(
            conn_input,
            conn_output,
            table_origin='stg_aneel_empreendimento_geracao_distribuida',
            columns=columns,
            columns_pk=['cd_empresa_distribuidora'],
            column_sk='sk_empresa_distribuidora',
            parquet=True,
        )

    def treat(self):
        r_cnpj = r'^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$'

        self.df_load = self.df_extract.assign(
            cd_empresa_distribuidora=lambda x: x.cd_empresa_distribuidora.str.upper(),
            no_empresa_distribuidora=lambda x: x.no_empresa_distribuidora.str.upper(),
            no_cnpj=lambda x: x.no_cnpj.apply(
                lambda y: _re.sub(r_cnpj, r"\1.\2.\3/\4-\5", y)),
        )

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str = 'emd',
        cd_empresa_distribuidora_origin: str = 'cd_empresa_distribuidora',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.cd_empresa_distribuidora = {as_origin}.{cd_empresa_distribuidora_origin}
        ;"""[5:-1]

        return sql
