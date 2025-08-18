from src.airflow.config.connection import Connection as _Connection
from src.airflow.factory.task_factory import TaskFactory as _TaskFactory
from src.airflow.config.task import Task as _Task
from src.airflow.connection.mongodb import MongoDB as _MongoDB
from src.airflow.connection.postgresql import PostgreSQL as _PostgreSQL

from etl.dw.base_mongo import TemplateBaseMongo as _TemplateBaseMongo


class ConfigTask(_Task):
    MONGO = 'MONGO'
    DEFAULT = 'DEFAULT'


class TaskFactory:
    def __init__(
        self,
        dw: type[_TemplateBaseMongo],
        config: type[_Task],
    ):
        self.dw = dw

        self.pool = config.POOL
        self.retries = config.RETRIES
        self.retry_delay = config.RETRY_DELAY
        self.deploy = config.DEPLOY
        self.config = config

        self.connection = _Connection(self.deploy)

    def _get_task_factory(self, dw: _TemplateBaseMongo) -> _TaskFactory:
        return _TaskFactory(
            task_id=dw.TABLE_NAME,
            func=dw.run,
            pool=self.pool,
            retries=self.retries,
            retry_delay=self.retry_delay,
        )

    def default(self):
        conn_id_postgres = self.connection.conn_dw

        dw = self.dw(
            conn_output=_PostgreSQL(conn_id_postgres).connect(),
        )

        return self._get_task_factory(dw)

    def mongo(self):
        conn_id_mongo = self.connection.conn_stage_mongodb
        conn_id_postgres = self.connection.conn_dw

        dw = self.dw(
            conn_input=_MongoDB(conn_id_mongo).connect(),
            conn_output=_PostgreSQL(conn_id_postgres).connect(),
        )

        return self._get_task_factory(dw)

    def get_task(self) -> _TaskFactory:
        funcs = {
            ConfigTask.MONGO: self.mongo,
            ConfigTask.DEFAULT: self.default
        }

        func = funcs.get(self.config.CONN)

        if not func:
            raise ValueError(self.config)

        return func()
