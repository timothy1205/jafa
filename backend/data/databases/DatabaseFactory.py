from backend.data.databases.AbstractDatabase import AbstractDatabase
from backend.data.databases.MongoDatabase import MongoDatabase


class DatabaseFactory:
    _databases = {}
    _cache = {}

    @staticmethod
    def create_database(database_type: str) -> AbstractDatabase:
        """Return the database associated with the provided type.

        Raises NotImplementedError if it doesn't exist.
        """
        if database_type in DatabaseFactory._databases:
            if database_type in DatabaseFactory._cache:
                return DatabaseFactory._cache[database_type]
            else:
                database = DatabaseFactory._databases[database_type]()
                DatabaseFactory._cache[database_type] = database
                return database
        else:
            raise NotImplementedError("Invalid database type given")

    @staticmethod
    def register_database(database_type, database_class):
        """Register a database string association."""
        DatabaseFactory._databases[database_type] = database_class


DatabaseFactory.register_database("mongo", MongoDatabase)
"""MongoDB"""
