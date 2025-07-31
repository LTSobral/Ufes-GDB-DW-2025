from pymongo import MongoClient as _MongoClient

from .base import Base as _Base


class MongoDB(_Base):
    """Gerencia conexões com o banco de dados MongoDB.

    Esta classe encapsula a lógica para estabelecer uma conexão com um servidor
    MongoDB, construindo a URI de conexão a partir de informações da instância
    e retornando um cliente `MongoClient`.

    Os atributos `username`, `password`, `host` e `port` são esperados
    como atributos da instância (e.g., definidos no `__init__` ou herdados
    da classe `_Base`).

    Atributos:
        URI (str): O modelo da URI de conexão para o MongoDB.
                   Contém placeholders `{USERNAME}`, `{PASSWORD}`, `{HOST}`,
                   e `{PORT}` que serão formatados com os atributos da instância.
    """

    URI = "mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin"

    def connect(self) -> _MongoClient:
        """Estabelece e retorna uma conexão com o servidor MongoDB.

        Este método constrói a URI de conexão utilizando os atributos de instância
        `username`, `password`, `host` e `port` (herdados ou definidos).
        Em seguida, inicializa e retorna uma instância do cliente
        `pymongo.MongoClient` com base nesta URI.

        Returns:
            _MongoClient: Uma instância do cliente MongoDB configurada e pronta para uso.

        Raises:
            Exception: Pode levantar exceções (e.g., `pymongo.errors.ConnectionFailure`)
                       se houver problemas ao se conectar ao banco de dados,
                       como credenciais inválidas ou servidor inacessível.
        """
        uri = self.URI.format(
            USERNAME=self.username,
            PASSWORD=self.password,
            HOST=self.host,
            PORT=self.port,
        )

        return _MongoClient(uri)

