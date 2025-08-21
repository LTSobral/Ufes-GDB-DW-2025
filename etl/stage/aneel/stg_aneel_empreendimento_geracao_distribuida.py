
from src.connection.mongodb import MongoDB as _MongoDB
from src.api.aneel.datastore.resource import (
    EmpreendimentoGeracaoDistribuida as _EmpreendimentoGeracaoDistribuida
)
from .base import Base as _Base

class StageAneelEmpreendimentoGeracaoDistribuida(_Base):
    def __init__(self, conn_output: _MongoDB) -> None:
        super().__init__(
            conn_output,
            _EmpreendimentoGeracaoDistribuida,
            "stg_aneel_empreendimento_geracao_distribuida"
        )