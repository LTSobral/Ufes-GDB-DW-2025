from typing import Callable as _Callable

from src.airflow.config.connection import Connection as _Connection
from src.airflow.factory.task_factory import TaskFactory as _TaskFactory
from src.airflow.config.task import Task as _Task
from src.airflow.connection.mongodb import MongoDB as _MongoDB

from etl.stage.aneel.base import TemplateBase as _TemplateBase


class TaskFactory:
    def __init__(
        self,
        stage: type[_TemplateBase],
        config: type[_Task],
    ):
        self.stage = stage

        self.deploy = True
        self.pool = config.POOL
        self.retries = config.RETRIES
        self.retry_delay = config.RETRY_DELAY
        self.deploy = config.DEPLOY

        self.config = _Connection(self.deploy)

    def _get_task_factory(self, stage: _TemplateBase):
        return _TaskFactory(
            task_id=stage.collection,
            func=stage.run,
            pool=self.pool,
            retries=self.retries,
            retry_delay=self.retry_delay,
        )

    def get_task(self) -> _TaskFactory:
        conn_id = _Connection().conn_stage_mongodb
        stage = self.stage(conn_output=_MongoDB(conn_id).connect())
        task_factory = self._get_task_factory(stage)

        return task_factory
