from airflow.hooks.base import BaseHook as _BaseHook
from airflow.models.connection import Connection as _Connection

from ...connection.base import Base as _Base


class Base:
    def __init__(
        self,
        conn_id: str,
    ) -> None:
        self.conn: _Connection = _BaseHook.get_connection(conn_id)

    def connect(self) -> _Base:
        raise NotImplementedError()
