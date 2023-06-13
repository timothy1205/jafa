from backend.data.databases.DatabaseFactory import DatabaseFactory
from pymongo.database import Database, Collection


class MongoMixin:

    def __init__(self):
        self.database: Database = DatabaseFactory.create_database(
            "mongo").get_client().jafa

    def _get_collection(self, colleciton_name: str) -> Collection:
        return self.database[colleciton_name]
