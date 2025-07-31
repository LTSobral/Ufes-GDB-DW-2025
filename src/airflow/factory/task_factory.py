from typing import (
    Any as _Any,
    Callable as _Callable,
)

from datetime import timedelta as _timedelta
from airflow.providers.standard.operators.python import PythonOperator as _Task


class TaskFactory:
    """Fábrica para criar instâncias de ``airflow.providers.standard.operators.python.PythonOperator``.

    Esta classe abstrai a criação de tarefas Airflow PythonOperator, padronizando a configuração
    de parâmetros comuns como ``pool``, ``execution_timeout`` e ``retry_delay``. Ela garante que
    as tarefas sejam criadas com um identificador padronizado e que a pool seja sempre definida.

    Atributos:
        _task_id (str): O identificador único da tarefa, convertido para maiúsculas.
        _func (Callable): A função Python a ser executada pela tarefa.
        _func_kwargs (dict[str, Any] | None): Argumentos de palavra-chave para a função `_func`.
        _pool (str): O nome da pool de recursos do Airflow à qual a tarefa pertence.
        _execution_timeout (timedelta | None): A duração máxima permitida para a execução da tarefa.
        _retry_delay (timedelta): O atraso entre tentativas de reexecução da tarefa em caso de falha.
        _kwargs (dict): Argumentos adicionais de palavra-chave passados diretamente para o ``PythonOperator``.
    """
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
        """Inicializa uma nova instância da fábrica de tarefas.

        Configura todos os parâmetros necessários para a criação posterior
        de um ``PythonOperator`` do Airflow.

        :param task_id: O identificador único da tarefa Airflow. Será convertido para maiúsculas.
        :type task_id: str
        :param func: A função Python que a tarefa executará.
        :type func: ~typing.Callable
        :param func_kwargs: Um dicionário de argumentos de palavra-chave a serem passados para ``func``.
            Pode ser ``None`` se a função não exigir argumentos.
        :type func_kwargs: dict[str, Any] | None
        :param pool: O nome da pool de recursos do Airflow para a tarefa.
        :type pool: str | None
        :param execution_timeout: Um dicionário com as palavras-chave para criar um ``timedelta``
            que define o tempo limite de execução da tarefa. Por exemplo: ``{'hours': 10}``.
            Se for ``None``, nenhum tempo limite será definido.
        :type execution_timeout: dict | None
        :param retry_delay: Um dicionário com as palavras-chave para criar um ``timedelta``
            que define o atraso entre tentativas de reexecução da tarefa em caso de falha.
            Por exemplo: ``{'minutes': 5}``. O padrão é 300 segundos (5 minutos) se ``None``.
        :type retry_delay: dict | None
        :param kwargs: Argumentos adicionais de palavra-chave que serão passados
            diretamente para o construtor da classe ``PythonOperator``. Valores ``None``
            nestes argumentos são ignorados.
        :type kwargs: Any
        :raises ValueError: Se a ``pool`` não for definida (fornecida como ``None`` ou string vazia).
        """
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
        """Cria e retorna uma instância configurada de ``PythonOperator``.

        A tarefa é construída usando os parâmetros fornecidos durante a
        inicialização da fábrica, garantindo que a ``pool``, ``execution_timeout``,
        e ``retry_delay`` sejam configurados conforme especificado.

        :returns: Uma instância de ``PythonOperator`` pronta para ser adicionada a um DAG.
        :rtype: ~airflow.providers.standard.operators.python.PythonOperator
        """
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
        """Propriedade: O identificador único da tarefa Airflow.

        :returns: O ``task_id`` da tarefa (em maiúsculas).
        :rtype: str
        """
        return self._task_id
    
    @property
    def task_func(self) -> _Callable:
        """Propriedade: A função Python que a tarefa executará.

        :returns: A função ``python_callable`` associada à tarefa.
        :rtype: ~typing.Callable
        """
        return self._func
    
    @property
    def task_pool(self) -> str:
        """Propriedade: O nome da pool de recursos do Airflow para a tarefa.

        :returns: A ``pool`` de recursos da tarefa.
        :rtype: str
        """
        return self._pool

