from requests import Response as _Response
from pymongo import MongoClient as _MongoClient

from src.api.aneel.datastore.resource import Resource as _Resource
from src.connection.mongodb import MongoDB as _MongoDB
from src.api.aneel.datastore.search import Search as _Search


class Base:
    schema = "stage"

    def __init__(
        self,
        conn_output: _MongoDB,
        resource: type[_Resource],
        collection: str,
        chunksize: int = 32000,
        database: str = 'stage'
    ) -> None:
        self.conn_output = conn_output
        self.resource = resource
        self.collection = collection
        self.chunksize = chunksize
        self.database = database

        self.data: list
        self.conn: _MongoClient
        self.page: _Response
        self.value_load: list[dict]

    def before(self):
        self.conn = self.conn_output.connect()
        db = self.conn[self.database]
        self._collection = db[self.collection]

        self.search = _Search(self.resource, self.chunksize)

    def extract(self):
        data = self.page.json()
        self.value_load = data.get('result', {'records': []}).get('records')

    def load(self):
        self._collection.insert_many(self.value_load)

    def run(self):
        self.before()
        for self.page in self.search.iterpage():
            self.extract()
            self.load()

class TemplateBase(Base):
    def __init__(self, conn_output: _MongoDB) -> None:
        raise NotImplementedError