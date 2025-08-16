# Importações de módulos internos/bibliotecas específicas do projeto
from src.airflow.config.connection import Connection as _Connection
from src.airflow.factory.task_factory import TaskFactory as _TaskFactory
from src.airflow.config.task import Task as _Task
from src.airflow.connection.mongodb import MongoDB as _MongoDB

# Importação de um módulo de estágio ETL específico
from etl.stage.aneel.base import TemplateBase as _TemplateBase


class TaskFactory:
    """
    Fábrica para criar objetos TaskFactory do Airflow, encapsulando
    a lógica de configuração e instanciação de tarefas específicas
    para estágios ETL (Extract, Transform, Load).

    Esta classe abstrai a complexidade de configurar uma tarefa
    do Airflow a partir de uma classe de estágio ETL, garantindo
    que as conexões e configurações de execução (pool, retries)
    sejam aplicadas corretamente.
    """

    def __init__(
        self,
        stage: type[_TemplateBase],
        config: type[_Task],
    ):
        """
        Inicializa a TaskFactory com as configurações necessárias
        para criar uma tarefa do Airflow.

        Define os parâmetros de execução da tarefa (pool, retries, etc.)
        com base na classe de configuração fornecida e prepara
        a infraestrutura de conexão para os estágios.

        :param stage: A classe do estágio ETL (subclasse de `_TemplateBase`)
                      que será executada pela tarefa. Esta classe
                      será instanciada no método `get_task`.
        :type stage: type[_TemplateBase]
        :param config: A classe de configuração da tarefa (subclasse de `_Task`)
                       que contém os parâmetros como POOL, RETRIES, RETRY_DELAY
                       e DEPLOY.
        :type config: type[_Task]
        """
        self.stage = stage

        self.pool = config.POOL
        self.retries = config.RETRIES
        self.retry_delay = config.RETRY_DELAY
        self.deploy = config.DEPLOY

        self.config = _Connection(self.deploy)

    def _get_task_factory(self, stage: _TemplateBase) -> _TaskFactory:
        """
        Cria e retorna uma instância de `_TaskFactory` do Airflow
        configurada para um estágio ETL específico.

        Este é um método auxiliar interno que mapeia os atributos
        de uma instância de estágio (como `collection` e `run`)
        para os parâmetros de uma `_TaskFactory` do Airflow,
        juntamente com as configurações de execução definidas na
        inicialização da `TaskFactory`.

        :param stage: A instância do objeto de estágio ETL (`_TemplateBase`)
                      que contém a lógica a ser executada pela tarefa
                      (método `run`) e o ID da coleção (`collection`).
        :type stage: _TemplateBase
        :returns: Um objeto `_TaskFactory` do Airflow pronto para
                  ser incluído em um DAG.
        :rtype: _TaskFactory
        """
        return _TaskFactory(
            task_id=stage.collection,
            func=stage.run,
            pool=self.pool,
            retries=self.retries,
            retry_delay=self.retry_delay,
        )

    def get_task(self) -> _TaskFactory:
        """
        Cria e retorna um objeto `_TaskFactory` do Airflow completo,
        pronto para ser utilizado em um DAG.

        Este método lida com a obtenção do ID da conexão MongoDB,
        instancia a classe de estágio configurada em `__init__`
        passando a conexão necessária (MongoDB), e então utiliza o método
        auxiliar `_get_task_factory` para construir a tarefa final.

        :returns: Um objeto `_TaskFactory` do Airflow totalmente configurado
                  para o estágio ETL definido, incluindo a lógica de execução
                  e os parâmetros do Airflow.
        :rtype: _TaskFactory
        """
        conn_id = _Connection().conn_stage_mongodb
        stage = self.stage(conn_output=_MongoDB(conn_id).connect())
        task_factory = self._get_task_factory(stage)

        return task_factory

