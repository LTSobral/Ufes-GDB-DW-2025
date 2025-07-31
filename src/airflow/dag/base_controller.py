from src.airflow.factory import TaskFactory as _TaskFactory

from src.airflow.factory.tasks import Tasks as _Tasks
from src.airflow.utils.normalize import (
    pascal_case_to_snake_case as _pascal_case_to_snake_case
)


class BaseController:
    def __init__(
        self,
        all_tasks: type[_Tasks] | list[type[_Tasks]],
        dag_id: str | None = None
    ) -> None:
        self.all_tasks = all_tasks
        self.dag_id = dag_id or f'dag_{_pascal_case_to_snake_case(self.__class__.__name__)}'

    @property
    def all_tasks(self):
        return self._all_tasks
    
    @all_tasks.setter
    def all_tasks(self, __value: type[_Tasks] | list[type[_Tasks]]):
        if isinstance(__value, type) and issubclass(__value, _Tasks):
            self._all_tasks = __value

        elif isinstance(__value, list) and all(isinstance(v, type) and issubclass(v, _Tasks) for v in __value):
            all_tasks = _Tasks
            all_tasks.TASKS = [
                t 
                for v in __value
                for t in v.TASKS
            ]

            all_tasks.DEPENDENCIES = {
                k: d
                for v in __value 
                for k, d in v.DEPENDENCIES.items()
            }

            self._all_tasks = all_tasks

    def get_tasks(self) -> list[_TaskFactory]:
        return [f() for f in self.all_tasks.TASKS]

    def get_dependencies(self) -> dict[str, list[str]]:
        tasks_id = [
            t.task_id if isinstance(t, _TaskFactory) else t.group_id
            for t in self.get_tasks()
        ]

        dependencies = {
            k: [
                d
                for d in (v if isinstance(v, list) else [v])
                if d.upper() in tasks_id
            ]
            for k, v in self.all_tasks.DEPENDENCIES.items()
        }

        return dependencies

    def params(self):
        return {
            'dag_id': self.dag_id,
            'children': self.get_tasks(),
            'dependencies': self.get_dependencies()
        }
