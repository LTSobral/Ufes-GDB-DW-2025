from .task_factory import (
    TaskFactory as _TaskFactory
)

from src.airflow.factory.tasks import Tasks as _Tasks
from src.airflow.config.pool import Pool as _Pool
from src.airflow.config.task import Task as _ConfigTask

from etl.stage.aneel import (
    StageAneelEmpreendimentoGeracaoDistribuida
)


class Config(_ConfigTask):
    POOL = _Pool.ANEEL


class StageAneelTasks(_Tasks):
    ALL_TASKS = {
        Config: [
            StageAneelEmpreendimentoGeracaoDistribuida,
        ]
    }

    TASKS = [
        _TaskFactory(s, k).get_task
        for k, v in ALL_TASKS.items()
        for s in v
    ]

    DEPENDENCIES = {}
