from requests import Response as _Response
from pymongo import MongoClient as _MongoClient

from src.api.aneel.datastore.resource import Resource as _Resource
from src.connection.mongodb import MongoDB as _MongoDB
from src.api.aneel.datastore.search import Search as _Search
from src.etl.utils.log import log as _log


class Base:
    """Classe base que implementa um fluxo de Extração e Carregamento (EL) para dados de API.

    Esta classe é projetada para buscar dados de uma API paginada e persistir esses dados
    em uma coleção MongoDB. Ela gerencia a conexão com o MongoDB, a lógica de busca
    de dados da API e o processo de inserção na base de dados.

    Attributes:
        schema (str): O esquema ou ambiente padrão para as operações de banco de dados.
                      Pode ser sobrescrito por instâncias ou subclasses.
    """
    schema = "stage"

    def __init__(
        self,
        conn_output: _MongoDB,
        resource: type[_Resource],
        collection: str,
        chunksize: int = 32000,
        database: str = 'stage'
    ) -> None:
        """Inicializa uma nova instância da classe Base.

        Configura os parâmetros essenciais para a conexão com o MongoDB, a definição
        do recurso de API a ser consultado e a estratégia de carregamento dos dados.

        Args:
            conn_output (_MongoDB): Objeto de conexão MongoDB pré-configurado.
            resource (type[_Resource]): A classe do recurso da API que define como
                                        os dados devem ser buscados.
            collection (str): O nome da coleção MongoDB onde os dados serão carregados.
            chunksize (int, optional): O tamanho dos blocos (chunks) de dados a serem
                                       buscados da API por página. Padrão para 32000.
            database (str, optional): O nome do banco de dados MongoDB a ser utilizado.
                                      Padrão para 'stage'.

        Attributes:
            conn_output (_MongoDB): Armazena o objeto de conexão MongoDB de saída.
            resource (type[_Resource]): Armazena a classe do recurso da API.
            collection (str): Armazena o nome da coleção MongoDB alvo.
            chunksize (int): Armazena o tamanho dos blocos de dados.
            database (str): Armazena o nome do banco de dados MongoDB alvo.
            data (list): Armazena dados temporariamente (não utilizado diretamente no fluxo atual).
            conn (_MongoClient): Conexão ativa com o cliente MongoDB, estabelecida em `before()`.
            page (_Response): A resposta HTTP da página atual da API, utilizada em `extract()`.
            value_load (list[dict]): Uma lista de dicionários contendo os registros
                                     extraídos prontos para carregamento.
        """
        self.conn_output = conn_output
        self.resource = resource
        self.collection = collection
        self.chunksize = chunksize
        self.database = database

        self.data: list
        self.conn: _MongoClient
        self.page: _Response
        self.value_load: list[dict]

    @_log
    def before(self) -> None:
        """Prepara a instância da classe antes da execução principal do processo EL.

        Este método estabelece a conexão com o banco de dados MongoDB, seleciona a
        coleção alvo e inicializa o objeto de busca de dados da API.

        Side Effects:
            Define `self.conn` com o cliente MongoDB conectado.
            Define `self._collection` com o objeto da coleção MongoDB alvo.
            Define `self.search` com uma nova instância de `_Search` configurada.
        """
        self.conn = self.conn_output.connect()
        db = self.conn[self.database]

        if self.collection in db.list_collection_names():
            db[self.collection].drop()

        self._collection = db[self.collection]

        self.search = _Search(self.resource, self.chunksize)

    @_log
    def extract(self) -> None:
        """Extrai os registros de dados da resposta JSON da página atual da API.

        Analisa o conteúdo JSON da resposta HTTP (`self.page`) e extrai a lista
        de registros (usualmente sob as chaves 'result' e 'records') para serem
        posteriormente carregados no banco de dados.

        Side Effects:
            Define `self.value_load` com a lista de dicionários extraídos da página.
            Se 'result' ou 'records' não forem encontrados, `self.value_load`
            será uma lista vazia, evitando erros.
        """
        data = self.page.json()
        self.value_load = data.get('result', {}).get('records', [])

    @_log
    def load(self) -> None:
        """Carrega os dados extraídos na coleção MongoDB configurada.

        Insere a lista de dicionários contida em `self.value_load` como documentos
        na coleção MongoDB (`self._collection`). Utiliza `insert_many` para
        otimizar a operação de inserção.

        Side Effects:
            Insere documentos no banco de dados MongoDB.
        """
        self._collection.insert_many(self.value_load)

    def run(self) -> None:
        """Executa o ciclo completo de extração e carregamento de dados.

        Este é o método principal que orquestra todo o processo EL.
        Ele primeiro chama `before()` para configurar, depois itera sobre
        todas as páginas de dados fornecidas pelo objeto `search`, chamando
        `extract()` para cada página e, em seguida, `load()` para persistir
        os dados extraídos.
        """
        self.before()
        for page in self.search.iterpage():
            self.page = page
            self.extract()
            self.load()

class TemplateBase(Base):
    """Classe base abstrata (template) para a criação de processadores de dados específicos.

    Esta classe herda de `Base` e é projetada para ser um esqueleto. Ela não deve
    ser instanciada diretamente. Subclasses devem implementar seu próprio construtor
    e, se necessário, sobrescrever outros métodos para adaptar o fluxo EL.
    """
    def __init__(self, conn_output: _MongoDB) -> None:
        """O construtor desta classe template não deve ser chamado diretamente.

        Subclasses de `TemplateBase` são obrigadas a implementar seu próprio método
        `__init__` para definir a lógica de inicialização específica.

        Args:
            conn_output (_MongoDB): Um objeto de conexão MongoDB. Este parâmetro
                                    está aqui para fins de compatibilidade de assinatura,
                                    mas o `__init__` levantará um erro.

        Raises:
            NotImplementedError: Sempre levantado para indicar que este construtor
                                 deve ser implementado por uma subclasse concreta.
        """
        raise NotImplementedError
