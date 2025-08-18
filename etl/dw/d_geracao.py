from typing_extensions import override as _override

from etl.dw.base_mongo import (
    BaseMongo as _BaseMongo,
    Column as _Column
)
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionGeracao(_BaseMongo):
    TABLE_NAME = 'd_geracao'

    def __init__(self, conn_input: _MongoDB, conn_output: _PostgreSQL):
        columns = [
            _Column('SigTipoGeracao', 'cd_tipo'),
            _Column('DscFonteGeracao', 'no_fonte'),
            _Column('DscPorte', 'no_porte'),
        ]

        super().__init__(
            conn_input,
            conn_output,
            table_origin='stg_aneel_empreendimento_geracao_distribuida',
            columns=columns,
            columns_pk=['cd_tipo', "no_fonte", "no_porte"],
            column_sk='sk_geracao',
            parquet=True,
        )

    def treat(self):
        ds_tipo = {
            "UTN": "USINA TERMONUCLEAR",
            "UTE": "USINA TERMELÉTRICA",
            "UHE": "USINA HIDRELÉTRICA",
            "UFV": "CENTRAL GERADORA SOLAR FOTOVOLTAICA",
            "PCH": "PEQUENA CENTRAL HIDRELÉTRICA",
            "EOL": "CENTRAL GERADORA EÓLICA",
            "CGU": "CENTRAL GERADORA UNDI-ELÉTRICA",
            "CGH": "CENTRAL GERADORA HIDRELÉTRICA",
        }

        self.df_load = self.df_extract.assign(
            cd_tipo=lambda x: x.cd_tipo.str.upper(),
            no_fonte=lambda x: x.no_fonte.str.upper(),
            no_porte=lambda x: x.no_porte.str.upper(),
            ds_tipo=lambda x: x.cd_tipo.apply(ds_tipo.get),
        )

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str='ger',
        cd_tipo_origin: str='cd_tipo',
        no_fonte_origin: str='no_fonte',
        no_porte_origin: str='no_porte',
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.cd_tipo = {as_origin}.{cd_tipo_origin}
                AND {as_dimension}.no_fonte = {as_origin}.{no_fonte_origin}
                AND {as_dimension}.no_porte = {as_origin}.{no_porte_origin}
        ;"""[5:-1]

        return sql