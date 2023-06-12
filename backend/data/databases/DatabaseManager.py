from backend.data.databases.AbstractDatabase import AbstractDatabase
from backend.data.databases.MongoDatabase import MongoDatabase
from backend.JafaConfig import JafaConfig


class MissingDatabaseClass(Exception):
    pass


class DatabaseManager:
    __database = None

    @staticmethod
    def __create_instance():
        config = JafaConfig()
        if config.database_type == "mongo":
            return MongoDatabase()
        elif config.database_type == "custom":
            if config.database_class == None:
                raise MissingDatabaseClass(
                    "Must set the field database_class to a valid class")

            return config.database_class()
        else:
            raise NotImplementedError("Invalid database type given")

    @staticmethod
    def get_instance(force_create=False) -> AbstractDatabase:
        """Singleton method for retrieving whichever database was configured"""
        if DatabaseManager.__database is None or force_create:
            DatabaseManager.__database = DatabaseManager.__create_instance()

        return DatabaseManager.__database
