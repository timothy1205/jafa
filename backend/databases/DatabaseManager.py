from backend.databases.AbstractDatabase import AbstractDatabase
from backend.databases.MongoDatabase import MongoDatabase


class DatabaseManager:
    __database = None

    @staticmethod
    def __create_instance():
        # TODO: Choose based on config
        return MongoDatabase()

    @staticmethod
    def get_instance() -> AbstractDatabase:
        """Singleton method for retrieving whichever database was configured"""
        if DatabaseManager.__database is None:
            DatabaseManager.__database = DatabaseManager.__create_instance()

        return DatabaseManager.__database
