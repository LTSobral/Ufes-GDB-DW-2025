from .base import Base as _Base
from ...connection.mongodb import MongoDB as _MongoDB


class MongoDB(_Base):
    """Representa um gerenciador de conexão para bancos de dados MongoDB.

    Esta classe estende `_Base` para abstrair a recuperação de detalhes de conexão
    através de um `conn_id` e facilitar a criação de instâncias do cliente MongoDB.

    Herda de:
        _Base: A classe base para gerenciamento de conexões, que provavelmente
               cuida da obtenção dos detalhes de conexão (`self.conn`) usando o `conn_id`.
    """

    def __init__(self, conn_id: str) -> None:
        """Inicializa uma nova instância do gerenciador de conexão MongoDB.

        Args:
            conn_id (str): O identificador único da conexão MongoDB. Este ID é usado para
                           recuperar os detalhes da conexão (host, porta, usuário, etc.)
                           através da classe base (`_Base`).
        """
        super().__init__(conn_id)
    
    def connect(self) -> _MongoDB:
        """Cria e retorna uma instância configurada do cliente MongoDB.

        Esta instância pode ser usada para interagir diretamente com o banco de dados MongoDB.
        Os detalhes da conexão (host, database, username, password, port) são obtidos
        do objeto `self.conn`, que é preenchido pela classe base durante a inicialização.

        Returns:
            _MongoDB: Uma instância do cliente MongoDB (da importação `from ...connection.mongodb import MongoDB`),
                      pronto para ser usado para operações de banco de dados.
        """
        if self.conn.conn_type != 'mongo':
            raise Exception(f'Conexão errada {self.conn.conn_type} {self.conn.conn_id}')

        mongodb = _MongoDB(
            host=self.conn.host,
            database=self.conn.schema,  # 'schema' geralmente mapeia para 'database' no MongoDB
            username=self.conn.login,
            password=self.conn.password,
            port=self.conn.port,
        )

        return mongodb

