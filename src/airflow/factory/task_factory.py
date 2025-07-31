from typing import (
    Any as _Any,
    Callable as _Callable,
)

from datetime import timedelta as _timedelta
from airflow.providers.standard.operators.python import PythonOperator as _Task


class TaskFactory:
    def __init__(
        self,
        task_id: str,
        func: _Callable,
        func_kwargs: dict[str, _Any] | None = None,
        pool: str | None = None,
        execution_timeout= {'hours' : 10},
        retry_delay = None,
        **kwargs
    ) -> None:
        self._task_id = task_id.upper()
        self._func = func
        self._func_kwargs = func_kwargs
        self._pool = pool
        
        if not self._pool:
            raise ValueError(
                f"A pool deve ser definida antes de criar a task `{self.task_id}`"
            )
        
        self._execution_timeout = (
            _timedelta(**execution_timeout)
            if execution_timeout is not None
            else None
        )
        
        self._retry_delay = (
            _timedelta(**retry_delay)
            if retry_delay is not None
            else _timedelta(seconds=300)
        )
        
        self._kwargs = {k: v for k, v in kwargs.items() if v is not None}

    def create_task(self) -> _Task:
        task = _Task(
            task_id=self._task_id,
            python_callable=self._func,
            op_kwargs=self._func_kwargs,
            pool=self._pool,
            execution_timeout=self._execution_timeout,
            retry_delay=self._retry_delay,
            **self._kwargs
        )

        return task
    
    @property
    def task_id(self) -> str:
        return self._task_id
    
    @property
    def task_func(self) -> _Callable:
        return self._func
    
    @property
    def task_pool(self) -> str:
        return self._pool
