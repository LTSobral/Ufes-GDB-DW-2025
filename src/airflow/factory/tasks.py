from typing import Callable as _Callable

from src.airflow.factory.task_factory import TaskFactory as _TaskFactory


class Tasks:
    TASKS: list[_Callable[[], _TaskFactory]]
    DEPENDENCIES: dict[str, list[str] | str]
