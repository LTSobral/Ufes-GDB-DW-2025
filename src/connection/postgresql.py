from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine import (
    URL as _URL,
    Engine as _Engine
)

from .base import Base as _Base

class PostgreSQL(_Base):
    URI = "postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    def connect(self) -> _Engine:
        """Estabelece e retorna uma engine de conexão com o servidor PostgreSQL.

        Este método constrói a URI de conexão utilizando os atributos de instância
        `username`, `password`, `host`, `port` e `database`.
        Em seguida, inicializa e retorna uma instância da `Engine` do SQLAlchemy
        com base nesta URI.

        A `Engine` é o ponto central de comunicação com o banco de dados e gerencia
        um pool de conexões.

        Returns:
            _Engine: Uma instância da Engine do SQLAlchemy configurada e pronta para uso.

        Raises:
            Exception: Pode levantar exceções (e.g., `sqlalchemy.exc.OperationalError`)
                       se houver problemas ao se conectar ao banco de dados,
                       como credenciais inválidas, banco de dados inexistente
                       ou servidor inacessível.
        """
        # A classe URL do SQLAlchemy ajuda a construir a URI de forma segura,
        # evitando problemas com caracteres especiais em senhas.
        uri = self.URI.format(
            USERNAME=self.username,
            PASSWORD=self.password,
            HOST=self.host,
            PORT=self.port,
            DATABASE=self.database
        )
        print(uri)
        engine: _Engine = _create_engine(uri, future=False)

        return engine
