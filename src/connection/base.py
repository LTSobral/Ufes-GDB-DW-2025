class Base:
    """Classe base abstrata para gerenciar parâmetros de conexão.

    Esta classe define uma interface comum e armazena os parâmetros
    básicos necessários para estabelecer uma conexão, como host, porta,
    nome de usuário e senha. Ela não implementa a lógica real de conexão,
    mas serve como um modelo para classes filhas que herdarão e
    implementarão o método `connect` para tipos específicos de conexão
    (ex: banco de dados, API, etc.).
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str | None = None
    ) -> None:
        """Inicializa uma nova instância da classe Base com os parâmetros de conexão.

        Args:
            host (str): O endereço do host ou IP do servidor ao qual se conectar.
            port (int): O número da porta para a conexão.
            username (str): O nome de usuário para autenticação.
            password (str): A senha para autenticação.
            database (str | None, optional): O nome do banco de dados específico a ser conectado.
                                            Se None, a conexão pode ser para um servidor genérico
                                            ou um banco de dados padrão. Padrão é None.
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database

    def connect(self):
        """Estabelece a conexão com o recurso.

        Este é um método abstrato que deve ser sobrescrito por qualquer subclasse
        que herde de `Base`. A implementação real da lógica de conexão
        (ex: conectar a um banco de dados, uma API, etc.) deve ser fornecida na subclasse.

        Raises:
            NotImplementedError: Sempre é levantada para indicar que o método
                                 ainda não foi implementado na classe base e
                                 precisa ser sobrescrito pelas subclasses.
        """
        raise NotImplementedError

