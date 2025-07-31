from .base import Base as _Base
from ...connection.mongodb import MongoDB as _MongoDB


class MongoDB(_Base):
    def __init__(self, conn_id: str) -> None:
        super().__init__(conn_id)
    
    def connect(self) -> _MongoDB:
        mongodb = _MongoDB(
            host=self.conn.host,
            database=self.conn.schema,
            username=self.conn.login,
            password=self.conn.password,
            port=self.conn.port,
        )

        return mongodb
