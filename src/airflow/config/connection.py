class Connection:
    """Gerencia as configurações de conexão para diferentes ambientes.

    Esta classe permite selecionar entre configurações de conexão de produção
    e desenvolvimento, fornecendo as strings de conexão apropriadas
    com base no ambiente de implantação.

    Atributos:
        config (Production | Development): A classe de configuração de ambiente selecionada.
        conn_stage_mongodb (str): A string de conexão para o banco de dados MongoDB de stage.
    """

    class Production:
        """Contém as configurações de conexão para o ambiente de Produção."""
        CONN_STAGE_MONGODB = "conn_stage_mongodb"
        """String de conexão para o banco de dados MongoDB de stage (produção)."""

    class Development:
        """Contém as configurações de conexão para o ambiente de Desenvolvimento."""
        CONN_STAGE_MONGODB = "conn_stage__dev__mongodb"
        """String de conexão para o banco de dados MongoDB de stage (desenvolvimento)."""
    
    def __init__(self, deploy: bool = True):
        """Inicializa uma nova instância da classe Connection.

        Seleciona automaticamente as configurações de conexão apropriadas
        (Produção ou Desenvolvimento) com base no valor do parâmetro `deploy`.

        Args:
            deploy (bool, optional): Se `True`, as configurações de Produção serão usadas.
                Se `False`, as configurações de Desenvolvimento serão usadas.
                Padrão é `True`.
        """
        self.config = self.Production if deploy else self.Development

        self.conn_stage_mongodb = self.config.CONN_STAGE_MONGODB

