from airflow.hooks.base import BaseHook as _BaseHook
from airflow.models.connection import Connection as _Connection

from ...connection.base import Base as _Base


class Base:
    """
    Classe base abstrata para gerenciar conexões Airflow com sistemas externos.

    Esta classe fornece a infraestrutura básica para acessar os detalhes de uma
    conexão Airflow configurada e define uma interface para estabelecer a conexão
    real com o serviço ou sistema externo.

    Subclasses devem implementar o método `connect()` para fornecer a lógica
    específica de conexão.
    """

    def __init__(
        self,
        conn_id: str,
    ) -> None:
        """
        Inicializa uma nova instância da classe base de conexão.

        Recupera os detalhes da conexão Airflow associada ao `conn_id` fornecido
        e os armazena como um atributo da instância para uso posterior.

        Args:
            conn_id (str): O ID da conexão Airflow a ser utilizada. Este ID
                           corresponde a uma conexão configurada na UI do Airflow.
        """
        self.conn: _Connection = _BaseHook.get_connection(conn_id)

    def connect(self) -> _Base:
        """
        Estabelece a conexão com o serviço ou sistema externo.

        Este método é abstrato e deve ser implementado por subclasses. A
        implementação deve conter a lógica para criar e retornar um objeto
        de conexão concreto que possa ser usado para interagir com o serviço
        externo (por exemplo, um cliente de banco de dados, um cliente de API, etc.).

        Raises:
            NotImplementedError: Se o método não for sobrescrito em uma subclasse.

        Returns:
            _Base: Um objeto de conexão concreto que estende ou implementa
                   a classe `...connection.base.Base`, representando a conexão
                   estabelecida.
        """
        raise NotImplementedError("O método 'connect()' deve ser implementado por subclasses.")

