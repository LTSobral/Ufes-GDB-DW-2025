from .base import Base as _Base
from ...connection.postgresql import PostgreSQL as _PostgreSQL


class PostgreSQL(_Base):
    def __init__(self, conn_id: str) -> None:
        super().__init__(conn_id)
    
    def connect(self) -> _PostgreSQL:
        if self.conn.conn_type != 'postgres':
            raise Exception(f'Conexão errada {self.conn.conn_type}-{self.conn.conn_id}')

        postgresql = _PostgreSQL(
            host=self.conn.host,
            database=self.conn.schema,
            username=self.conn.login,
            password=self.conn.password,
            port=self.conn.port,
        )
        return postgresql

