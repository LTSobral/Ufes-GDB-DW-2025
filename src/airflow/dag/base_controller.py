from src.airflow.factory import TaskFactory as _TaskFactory

from src.airflow.factory.tasks import Tasks as _Tasks
from src.airflow.utils.normalize import (
    pascal_case_to_snake_case as _pascal_case_to_snake_case
)


class BaseController:
    """Controlador base para a criação de DAGs do Apache Airflow.

    Esta classe abstrai a lógica de agrupamento de tarefas, resolução de dependências
    e geração de parâmetros necessários para a construção de um objeto `DAG`.
    É projetada para ser herdada por controladores específicos de domínios ou DAGs.
    """
    def __init__(
        self,
        all_tasks: type[_Tasks] | list[type[_Tasks]],
        dag_id: str | None = None
    ) -> None:
        """Inicializa uma nova instância do controlador base.

        Args:
            all_tasks (type[_Tasks] | list[type[_Tasks]]):
                A classe `_Tasks` contendo as tarefas e dependências, ou uma lista
                de classes `_Tasks` a serem combinadas.
            dag_id (str, optional):
                O ID da DAG. Se `None`, será gerado a partir do nome da classe do controlador
                no formato snake_case (e.g., 'MyController' -> 'dag_my_controller').
                Padrão para `None`.
        """
        self.all_tasks = all_tasks
        self.dag_id = dag_id or f'dag_{_pascal_case_to_snake_case(self.__class__.__name__)}'

    @property
    def all_tasks(self) -> type[_Tasks]:
        """Retorna a classe `_Tasks` agregada.

        Returns:
            type[_Tasks]: A classe `_Tasks` que contém todas as tarefas e dependências processadas.
        """
        return self._all_tasks
    
    @all_tasks.setter
    def all_tasks(self, __value: type[_Tasks] | list[type[_Tasks]]):
        """Define a classe `_Tasks` ou agrega uma lista delas.

        Se uma lista de classes `_Tasks` for fornecida, suas tarefas e dependências
        serão combinadas em uma única classe `_Tasks` interna para uso posterior.

        Args:
            __value (type[_Tasks] | list[type[_Tasks]]):
                A classe `_Tasks` a ser definida ou uma lista de classes `_Tasks`
                para serem agregadas.
        """
        if isinstance(__value, type) and issubclass(__value, _Tasks):
            self._all_tasks = __value

        elif isinstance(__value, list) and all(isinstance(v, type) and issubclass(v, _Tasks) for v in __value):
            # Cria uma nova instância de _Tasks para combinar tudo
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
        # else:
        #     Considerar levantar um TypeError aqui para valores inválidos.

    def get_tasks(self) -> list[_TaskFactory]:
        """Obtém uma lista de instâncias de tarefas.

        Itera sobre as definições de tarefas na classe `all_tasks.TASKS` e as instancia
        como objetos `_TaskFactory`, que representam as tarefas prontas para serem
        adicionadas a uma DAG do Airflow.

        Returns:
            list[_TaskFactory]: Uma lista de instâncias de `_TaskFactory`.
        """
        return [f() for f in self.all_tasks.TASKS]

    def get_dependencies(self) -> dict[str, list[str]]:
        """Obtém um dicionário de dependências entre tarefas.

        Processa as dependências definidas em `all_tasks.DEPENDENCIES`, garantindo
        que apenas as dependências para tarefas existentes (cujos IDs estão entre
        as tarefas geradas por `get_tasks()`) sejam incluídas. As chaves do dicionário
        são os IDs das tarefas e os valores são listas de IDs de tarefas das quais
        a chave depende.

        Returns:
            dict[str, list[str]]: Um dicionário onde as chaves são IDs de tarefas
                                   e os valores são listas de IDs de tarefas das
                                   quais a chave depende.
        """
        tasks_id = [
            t.task_id if isinstance(t, _TaskFactory) else t.group_id
            for t in self.get_tasks()
        ]

        dependencies = {
            k: [
                d
                for d in (v if isinstance(v, list) else [v])
                if d.upper() in tasks_id # Assume que IDs de dependência são maiúsculos para comparação
            ]
            for k, v in self.all_tasks.DEPENDENCIES.items()
        }

        return dependencies

    def params(self) -> dict:
        """Gera um dicionário de parâmetros para a criação de uma DAG do Airflow.

        Combina o `dag_id` definido no controlador, as tarefas instanciadas via
        `get_tasks()` e as dependências resolvidas via `get_dependencies()`
        em um único dicionário, pronto para ser usado na construção de uma DAG
        do Apache Airflow.

        Returns:
            dict: Um dicionário contendo:
                - 'dag_id' (str): O ID único da DAG.
                - 'children' (list[_TaskFactory]): Uma lista de instâncias de tarefas.
                - 'dependencies' (dict[str, list[str]]): Um dicionário de dependências entre tarefas.
        """
        return {
            'dag_id': self.dag_id,
            'children': self.get_tasks(),
            'dependencies': self.get_dependencies()
        }

