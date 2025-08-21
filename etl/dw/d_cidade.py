from typing_extensions import override as _override

from etl.dw.base_mongo import (
    BaseMongo as _BaseMongo,
    Column as _Column
)
from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL


class DimensionCidade(_BaseMongo):
    TABLE_NAME = 'd_cidade'

    def __init__(self, conn_input: _MongoDB, conn_output: _PostgreSQL):
        columns = [
            _Column('CodMunicipioIbge', 'cd_cidade'),
            _Column('NomMunicipio', 'no_cidade'),
            _Column('SigUF', 'cd_estado'),
            _Column('NomRegiao', 'no_regiao'),
        ]

        super().__init__(
            conn_input,
            conn_output,
            table_origin='stg_aneel_empreendimento_geracao_distribuida',
            columns=columns,
            columns_pk=['cd_cidade'],
            column_sk='sk_cidade',
            parquet=True,
        )

    def treat(self):
        estados_brasileiros = {
            'AC': 'Acre',
            'AL': 'Alagoas',
            'AP': 'Amapá',
            'AM': 'Amazonas',
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal',
            'ES': 'Espírito Santo',
            'GO': 'Goiás',
            'MA': 'Maranhão',
            'MT': 'Mato Grosso',
            'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais',
            'PA': 'Pará',
            'PB': 'Paraíba',
            'PR': 'Paraná',
            'PE': 'Pernambuco',
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia',
            'RR': 'Roraima',
            'SC': 'Santa Catarina',
            'SP': 'São Paulo',
            'SE': 'Sergipe',
            'TO': 'Tocantins'
        }

        self.df_load = self.df_extract.assign(
            no_estado=lambda x: x.cd_estado.apply(estados_brasileiros.get)
        )

    def extract(self):
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
                "$addFields": {
                    "vl_latitude": {
                        "$convert": {
                            "input": {
                                "$replaceOne": {
                                    "input": "$NumCoordNEmpreendimento",
                                    "find": ",",
                                    "replacement": "."
                                }
                            },
                            "to": "double",
                            "onError": None,
                            "onNull": None
                        }
                    },
                    "vl_longitude": {
                        "$convert": {
                            "input": {
                                "$replaceOne": {
                                    "input": "$NumCoordEEmpreendimento",
                                    "find": ",",
                                    "replacement": "."
                                }
                            },
                            "to": "double",
                            "onError": None,
                            "onNull": None
                        }
                    },
                }
            },
            {
                '$group': {
                    '_id': {
                        c.name_dimesion: f'${c.name_origin}'
                        for c in self.columns
                    },
                    "vl_latitude": {
                        "$median": {
                            "input": "$vl_latitude",
                            "method": "approximate"
                        }
                    },
                    "vl_longitude": {
                        "$median": {
                            "input": "$vl_longitude",
                            "method": "approximate"
                        },
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    "vl_latitude": 1,
                    "vl_longitude": 1,
                } | {
                    c.name_dimesion: f'$_id.{c.name_dimesion}'
                    for c in self.columns
                }
            }
        ]

        colletion = self._conn_input[self.database][self.table_origin]
        self.cursor = colletion.aggregate(pipeline)

    @_override
    @classmethod
    def join(
        cls,
        as_origin: str,
        as_dimension: str = 'cid',
        cd_cidade_origin: str = 'cd_cidade'
    ):
        sql = f"""--sql
            LEFT JOIN '{cls.path().absolute()}' {as_dimension}
                ON {as_dimension}.cd_cidade = {as_origin}.{cd_cidade_origin}
        ;"""[5:-1]

        return sql
