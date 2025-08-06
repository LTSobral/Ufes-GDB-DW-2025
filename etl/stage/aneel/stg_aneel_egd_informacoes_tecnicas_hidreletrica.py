
from src.connection.mongodb import MongoDB as _MongoDB
from src.api.aneel.datastore.resource import (
    EGDInformacoesTecnicasHidreletrica as _EGDInformacoesTecnicasHidreletrica
)
from .base import Base as _Base

class StageAneelEGDInformacoesTecnicasHidreletrica(_Base):
    def __init__(self, conn_output: _MongoDB) -> None:
        super().__init__(
            conn_output,
            _EGDInformacoesTecnicasHidreletrica,
            "stg_aneel_egd_informacoes_tecnicas_hidreletrica"
        )

