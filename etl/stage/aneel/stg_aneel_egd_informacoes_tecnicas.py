
from src.connection.mongodb import MongoDB as _MongoDB


class StageAneelEGDInformacoesTecnicas:
    def __init__(self, conn_output: _MongoDB) -> None:
        self.conn_output = conn_output

        self.database = 'stage'
        self.table_origin = 'stg_aneel_egd_informacoes_tecnicas_fotovoltaica'
        self.collection = 'stg_aneel_egd_informacoes_tecnicas'

    def load(self):
        colletion = self._conn_output[self.database][self.table_origin]

        pipeline = [
            {
                "$unionWith":
                "stg_aneel_egd_informacoes_tecnicas_eolica"
            },
            {
                "$unionWith":
                "stg_aneel_egd_informacoes_tecnicas_hidreletrica"
            },
            {
                "$unionWith":
                "stg_aneel_egd_informacoes_tecnicas_termeletrica"
            },
            {
                "$project": {
                    "_id": 0
                }
            },
            {
                "$match": {"CodGeracaoDistribuida": {"$ne": ""}}
            },
            {
                "$addFields": {
                    "nu_competencia_conexao": {
                        "$dateToString": {
                            "format": "%Y%m",
                            "date": {
                                "$dateFromString": {
                                    "dateString": "$DatConexao"
                                }
                            }
                        }
                    }
                }
            },
            {
                "$out": {
                    "db": self.database,
                    "coll": self.collection
                }
            }
        ]

        self.cursor = colletion.aggregate(pipeline)

    def before_run(self):
        self._conn_output = self.conn_output.connect()

    def after_run(self):
        collection = self._conn_output[self.database][self.table_origin]

        collection.create_index([('CodGeracaoDistribuida', 1)])

    def run(self):
        self.before_run()
        self.load()
