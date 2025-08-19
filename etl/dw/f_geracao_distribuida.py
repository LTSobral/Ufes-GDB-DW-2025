import pandas as _pd
import duckdb as _ddb

from pathlib import Path as _Path
from datetime import datetime as _dt
from pytz import timezone as _timezone

from src.connection.mongodb import MongoDB as _MongoDB
from src.connection.postgresql import PostgreSQL as _PostgreSQL

from .d_cidade import DimensionCidade
from .d_grupo_tarifario import DimensionGrupoTarifario
from .d_tipo_consumidor import DimensionTipoConsumidor
from .d_competencia import DimensionCompetencia
from .d_empresa_distribuidora import DimensionEmpresaDistribuidora
from .d_geracao import DimensionGeracao


class FactGeracaoDistribuida:
    DEFAULT_PATH: _Path = _Path('./source/dim')

    TABLE_NAME: str = 'f_geracao_distribuida'

    def __init__(
        self,
        conn_input: _MongoDB,
        conn_output: _PostgreSQL,
        schema: str = 'dw',
        database: str = 'stage',
        chunksize: int = 40000,
    ) -> None:
        self.conn_input = conn_input
        self.table_name = self.__class__.TABLE_NAME
        self.table_origin = 'stg_aneel_empreendimento_geracao_distribuida'
        self.database = database
        self.chunksize = chunksize
        self.schema = schema
        self.conn_output = conn_output

        self.df_extract: _pd.DataFrame
        
        self.cidade = None
        self.classe_consumo = None
        self.competencia = None
        self.empresa_distribuidora = None
        self.geracao = None
        self.dt_update = _dt.now(_timezone('America/Sao_Paulo'))

    def extract(self):
        colletion = self._conn_input[self.database][self.table_origin]

        pipeline = [
            {
                "$addFields": {
                    "vl_potencia_instalada": {
                        "$toDouble": {
                            "$replaceOne": {
                                "input": "$MdaPotenciaInstaladaKW",
                                "find": ",",
                                "replacement": "."
                            }
                        }
                    },
                    "nu_competencia": {
                        "$dateToString": {
                            "format": "%Y%m",
                            "date": {
                                "$dateFromString": {
                                "dateString": "$DthAtualizaCadastralEmpreend"
                                }
                            }
                        }
                    }
                }
            },
            {
                "$lookup": {
                "from": "stg_aneel_egd_informacoes_tecnicas",
                "localField": "CodEmpreendimento",
                "foreignField": "CodGeracaoDistribuida",
                "pipeline": [
                    {
                    "$project": {
                        "_id": 0,
                        "nu_competencia_conexao": 1,
                        "QtdModulos": 1,
                    }
                    }
                ],
                "as": "tecnicas"
                }
            },
            {
                "$addFields": {
                    "nu_competencia_conexao": {
                        "$arrayElemAt": ["$tecnicas.nu_competencia_conexao", 0]
                    },
                    "qt_modulos": {
                        "$arrayElemAt": ["$tecnicas.QtdModulos", 0]
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "cd_cidade": "$CodMunicipioIbge",
                        "no_classe_consumo": "$DscClasseConsumo",
                        "cd_grupo_tarifario": "$DscSubGrupoTarifario",
                        "nu_competencia": "$nu_competencia",
                        "cd_empresa_distribuidora": "$SigAgente",
                        "cd_tipo": "$SigTipoGeracao",
                        "no_fonte": "$DscFonteGeracao",
                        "no_porte": "$DscPorte",
                        "nu_competencia_conexao": "$nu_competencia_conexao",
                        "cd_tipo_consumidor": "$SigTipoConsumidor",
                    },
                    "vl_potencia_instalada": {
                        "$sum": "$vl_potencia_instalada",
                    },
                    "qt_modulos": {
                        "$sum": "$qt_modulos",
                    },
                    "qt_empreendimentos": {
                        "$sum": 1,
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    "vl_potencia_instalada": 1,
                    "qt_modulos": 1,
                    "qt_empreendimentos": 1,
                    "cd_cidade": '$_id.cd_cidade',
                    "no_classe_consumo": '$_id.no_classe_consumo',
                    "cd_grupo_tarifario": '$_id.cd_grupo_tarifario',
                    "nu_competencia": '$_id.nu_competencia',
                    "cd_empresa_distribuidora": '$_id.cd_empresa_distribuidora',
                    "cd_tipo": '$_id.cd_tipo',
                    "cd_tipo_consumidor": '$_id.cd_tipo_consumidor',
                    "no_fonte": '$_id.no_fonte',
                    "no_porte": '$_id.no_porte',
                    "nu_competencia_conexao": '$_id.nu_competencia_conexao',
                }
            },
        ]

        self.cursor = colletion.aggregate(pipeline)

    def before_run(self):
        self._conn_output = self.conn_output.connect()
        self._conn_input = self.conn_input.connect()
        self.conn_duckdb = _ddb.connect(database=':memory:')

    def itercursor(self):
        _list = []
        i = 0
        for i, c in enumerate(self.cursor, 1):
            _list.extend([c])
            if i % self.chunksize == 0:
                yield _pd.DataFrame(_list)
                _list = []

        yield _pd.DataFrame(_list)

    def treat(self):
        df_extract = self.df_extract.assign(
            no_classe_consumo=lambda x: x.no_classe_consumo.str.upper(),
            cd_grupo_tarifario=lambda x: x.cd_grupo_tarifario.str.upper(),
            cd_empresa_distribuidora=lambda x: x.cd_empresa_distribuidora.str.upper(),
            cd_tipo=lambda x: x.cd_tipo.str.upper(),
            cd_tipo_consumidor=lambda x: x.cd_tipo_consumidor.str.upper(),
            no_fonte=lambda x: x.no_fonte.str.upper(),
            no_porte=lambda x: x.no_porte.str.upper(),
        )

        sql = f"""--sql
            SELECT 
                COALESCE(tc.sk_tipo_consumidor, '-3') sk_tipo_consumidor
                , COALESCE(gc.sk_grupo_tarifario, '-3') sk_grupo_tarifario
                , COALESCE(emd.sk_empresa_distribuidora, '-3') sk_empresa_distribuidora
                , COALESCE(cid.sk_cidade, '-3') sk_cidade
                , COALESCE(ger.sk_geracao, '-3') sk_geracao
                , COALESCE(dat.sk_competencia, '-3') sk_competencia_cadastro
                , COALESCE(comp_conexao.sk_competencia, '-3') sk_competencia_instalacao
                , COALESCE(flt.vl_potencia_instalada, 0) vl_potencia_instalada
                , COALESCE(flt.qt_modulos, 0) qt_modulos
                , COALESCE(flt.qt_empreendimentos, 0) qt_empreendimentos
            FROM df_extract flt
            {DimensionCidade.join('flt')}
            {DimensionGrupoTarifario.join('flt')}
            {DimensionTipoConsumidor.join('flt')}
            {DimensionCompetencia.join('flt')}
            {DimensionCompetencia.join('flt', 'comp_conexao', 'nu_competencia_conexao')}
            {DimensionEmpresaDistribuidora.join('flt')}
            {DimensionGeracao.join('flt')}
        ;"""[5:-1]
        self.df_load = self.conn_duckdb.sql(sql).df()

    def set_dt(self):
        self.df_load['dt_atualizacao'] = self.dt_update

    def load(self):
        self.df_load.to_sql(
            self.table_name,
            self._conn_output,
            index=False,
            schema=self.schema,
            if_exists='append',
        )

    def truncate(self):
        self._conn_output.execute(f'--sql TRUNCATE TABLE {self.schema}.{self.table_name} ;'[5:-1])

    def run(self):
        self.before_run()
        self.extract()
        self.truncate()
        for self.df_extract in self.itercursor():
            if not self.df_extract.empty:
                self.treat()
                self.set_dt()
                self.load()
