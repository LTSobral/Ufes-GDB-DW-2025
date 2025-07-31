import datetime as _dt

from typing import Any
from airflow.sdk.definitions.dag import (
    DAG as _DAG,
    ScheduleArg as _ScheduleArg,
)
from airflow.utils import timezone

from src.airflow.factory.task_factory import TaskFactory as _TaskFactory

class DAGFactory:
    DEFAULT_ARGS = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email': None,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'catchup': False,
        'retry_delay': _dt.timedelta(minutes=5),
    }
    def __init__(
        self,
        dag_id: str,
        children: list[_TaskFactory],
        default_args: dict[str, Any] | None = None,
        description: str | None = None,
        max_active_runs: int = 1,
        start_date: _dt.datetime | None = None,
        schedule: _ScheduleArg | None = None,
        tags: list[str] | None = None,
        dependencies: dict[str, list[str]] | None = None,
        **kwargs
    ) -> None:
        self._dag_id = dag_id.upper()
        self._children = children
        self._default_args = self.DEFAULT_ARGS | (default_args or {})
        self._description = description
        self._dependencies = dependencies
        self._max_active_runs = max_active_runs
        self._start_date = start_date or self._days_ago(1)
        self._schedule = schedule
        self._tags = [t.upper() for t in tags] if tags is not None else tags
        self._kwargs = kwargs

    @staticmethod
    def _days_ago(n, hour=0, minute=0, second=0, microsecond=0):
        """
        Get a datetime object representing `n` days ago. By default the time is
        set to midnight.
        """
        today = timezone.utcnow().replace(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond)
        return today - _dt.timedelta(days=n)

    def create_dag(self) -> _DAG:
        with _DAG(
            dag_id=self._dag_id,
            default_args=self._default_args,
            description=self._description,
            max_active_runs=self._max_active_runs,
            start_date=self._start_date,
            schedule=self._schedule,
            tags=self._tags,
            **self._kwargs
        ) as dag:
            for c in self._children:
                if isinstance(c, (_TaskFactory)):
                    c.create_task()
                else:
                    raise TypeError(f"Tipo de filho '{c}' inválido.")

            if self._dependencies is not None:
                for task_id, list_task_id_depen in self._dependencies.items():
                    task_right = dag.task_group.get_child_by_label(
                        task_id.upper())
                    for task_id_depen in list_task_id_depen:
                        task_left = dag.task_group.get_child_by_label(
                            task_id_depen.upper())
                        task_left >> task_right

        return dag

    @property
    def dag_id(self) -> str:
        return self._dag_id
