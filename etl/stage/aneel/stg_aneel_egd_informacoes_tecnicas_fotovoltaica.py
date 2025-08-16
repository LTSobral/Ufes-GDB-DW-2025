
from src.connection.mongodb import MongoDB as _MongoDB
from src.api.aneel.datastore.resource import (
    EGDInformacoesTecnicasFotovoltaica as _EGDInformacoesTecnicasFotovoltaica
)
from .base import Base as _Base

class StageAneelEGDInformacoesTecnicasFotovoltaica(_Base):
    def __init__(self, conn_output: _MongoDB) -> None:
        super().__init__(
            conn_output,
            _EGDInformacoesTecnicasFotovoltaica,
            "stg_aneel_egd_informacoes_tecnicas_fotovoltaica"
        )

