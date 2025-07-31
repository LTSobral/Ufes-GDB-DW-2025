class Base:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str | None = None
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database

    def connect(self):
        raise NotImplementedError