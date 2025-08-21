from typing import Callable as _Callable

from src.airflow.factory.task_factory import TaskFactory as _TaskFactory


class Tasks:
    """
    Define e gerencia as tarefas e suas dependências para um DAG (Directed Acyclic Graph)
    no Airflow.

    Esta classe atua como um repositório centralizado para as definições de tarefas
    e a lógica de orquestração entre elas, facilitando a criação e manutenção de fluxos
    de trabalho complexos no Airflow.
    """

    TASKS: list[_Callable[[], _TaskFactory]]
    """
    Lista de callables que produzem instâncias de TaskFactory.

    Cada elemento nesta lista é uma função (ou callable) que não recebe argumentos
    e retorna um objeto `_TaskFactory`. Estes objetos `_TaskFactory` são usados
    para configurar e gerar as tarefas reais do Airflow.
    Permite uma gestão flexível da criação de tarefas, encapsulando a lógica de
    construção de cada uma.
    """

    DEPENDENCIES: dict[str, list[str] | str]
    """
    Dicionário que define as dependências entre as tarefas.

    As chaves do dicionário representam o ID (ou nome) da tarefa que possui
    dependências. Os valores podem ser:
    - Uma string: O ID da tarefa da qual a chave depende.
    - Uma lista de strings: Uma lista de IDs de tarefas das quais a chave depende.

    Isso permite especificar que uma tarefa só pode ser executada após a conclusão
    de uma ou mais tarefas predecessoras. Os IDs das tarefas devem corresponder aos
    nomes das tarefas geradas pelas `_TaskFactory` em `TASKS`.

    Exemplos:
        - `{"task_B": "task_A"}` significa que "task_B" depende de "task_A".
        - `{"task_C": ["task_A", "task_B"]}` significa que "task_C" depende de "task_A" E "task_B".
    """

