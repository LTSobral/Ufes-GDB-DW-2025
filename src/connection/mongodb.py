from pymongo import MongoClient as _MongoClient

from .base import Base as _Base


class MongoDB(_Base):
    URI = "mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin"

    def connect(self) -> _MongoClient:
        uri = self.URI.format(
            USERNAME=self.username,
            PASSWORD=self.password,
            HOST=self.host,
            PORT=self.port,
        )

        return _MongoClient(uri)