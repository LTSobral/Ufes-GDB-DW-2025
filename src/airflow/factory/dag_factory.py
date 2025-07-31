import datetime as _dt

from typing import Any
from airflow.sdk.definitions.dag import (
    DAG as _DAG,
    ScheduleArg as _ScheduleArg,
)
from airflow.utils import timezone

from src.airflow.factory.task_factory import TaskFactory as _TaskFactory

class DAGFactory:
    """
    Fábrica para criar e configurar objetos DAG do Apache Airflow.

    Esta classe abstrai e simplifica o processo de criação de DAGs no Airflow,
    permitindo definir suas propriedades básicas, como ID, argumentos padrão,
    descrição, agendamento, e, mais importante, as tarefas (através de TaskFactory)
    e suas dependências.

    Atributos de Classe:
        DEFAULT_ARGS (dict): Argumentos padrão que são aplicados a todas as DAGs
                             criadas por esta fábrica, a menos que sejam sobrescritos
                             nos argumentos de inicialização.
    """
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
        """
        Inicializa uma nova instância de DAGFactory.

        Args:
            dag_id (str): O identificador único da DAG. Será convertido para maiúsculas.
            children (list[_TaskFactory]): Uma lista de instâncias de TaskFactory,
                                            cada uma responsável por criar uma tarefa
                                            dentro da DAG.
            default_args (dict[str, Any] | None): Um dicionário de argumentos padrão
                                                  para a DAG. Se fornecido, ele será
                                                  mesclado com e poderá sobrescrever
                                                  os DEFAULT_ARGS da classe.
            description (str | None): Uma breve descrição da DAG.
            max_active_runs (int): O número máximo de execuções ativas simultâneas permitidas para a DAG.
                                   Padrão é 1.
            start_date (_dt.datetime | None): A data e hora a partir da qual a DAG
                                              começará a ser agendada. Se None,
                                              define para um dia atrás em UTC.
            schedule (_ScheduleArg | None): O agendamento da DAG. Pode ser um cron string,
                                           um timedelta, None para agendamento manual, etc.
            tags (list[str] | None): Uma lista de tags para categorizar a DAG na UI do Airflow.
                                     As tags serão convertidas para maiúsculas.
            dependencies (dict[str, list[str]] | None): Um dicionário que define as dependências
                                                       entre as tarefas. A chave é o ID da tarefa
                                                       "direita" (dependente) e o valor é uma lista
                                                       de IDs de tarefas "esquerda" (que devem ser
                                                       concluídas primeiro). Por exemplo:
                                                       `{"tarefa_b": ["tarefa_a"]}` significa que
                                                       `tarefa_a` deve ser concluída antes de `tarefa_b`.
            **kwargs: Argumentos adicionais que serão passados diretamente para o construtor da DAG
                      do Airflow (ex: render_template_as_native_obj).
        """
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
        Retorna um objeto datetime representando `n` dias atrás.

        Por padrão, a hora é definida para meia-noite (00:00:00) em UTC.
        É útil para definir `start_date` em DAGs do Airflow de forma consistente.

        Args:
            n (int): O número de dias no passado.
            hour (int): A hora do dia (0-23). Padrão é 0.
            minute (int): O minuto da hora (0-59). Padrão é 0.
            second (int): O segundo do minuto (0-59). Padrão é 0.
            microsecond (int): O microssegundo do segundo (0-999999). Padrão é 0.

        Returns:
            _dt.datetime: Um objeto datetime em UTC representando a data e hora calculadas.
        """
        today = timezone.utcnow().replace(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond)
        return today - _dt.timedelta(days=n)

    def create_dag(self) -> _DAG:
        """
        Cria e configura um objeto DAG do Apache Airflow.

        Este método constrói a DAG utilizando os parâmetros definidos na inicialização
        da fábrica. Ele itera sobre os `children` (TaskFactory) para criar as tarefas
        e, se `dependencies` forem fornecidas, estabelece as relações de ordem entre
        as tarefas.

        Raises:
            TypeError: Se um item na lista `children` não for uma instância de `_TaskFactory`.

        Returns:
            _DAG: O objeto DAG do Airflow totalmente configurado e pronto para ser registrado.
        """
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
                    raise TypeError(f"Tipo de filho '{c}' inválido. Esperado _TaskFactory.")

            if self._dependencies is not None:
                for task_id, list_task_id_depen in self._dependencies.items():
                    # Garante que os IDs das tarefas sejam maiúsculos para corresponder ao padrão do Airflow/TaskFactory
                    task_right = dag.task_group.get_child_by_label(
                        task_id.upper())
                    for task_id_depen in list_task_id_depen:
                        task_left = dag.task_group.get_child_by_label(
                            task_id_depen.upper())
                        task_left >> task_right

        return dag

    @property
    def dag_id(self) -> str:
        """
        Retorna o ID único da DAG que será criada por esta fábrica.

        Returns:
            str: O ID da DAG.
        """
        return self._dag_id

