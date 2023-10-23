from typing import Optional

from pymongo import MongoClient

from backend.data.databases.AbstractDatabase import AbstractDatabase


class MongoDatabase(AbstractDatabase):
    def __init__(self):
        self.__client = None
        self.__db = None

    def connect(self, hostname: str, port=27017, username=None, password=None):
        """Connect via Mongo URI

        If username or password is None, its excluded from the URI.
        """
        if username is None or password is None:
            self.__client = MongoClient(f"mongodb://{hostname}:{port}")
        else:
            self.__client = MongoClient(
                f"mongodb://{username}:{password}@{hostname}:{port}"
            )

        self.__db = self.__client.jafa

    def setup(self):
        """Apply indexes"""
        self.__db["users"].create_index("username", unique=True)

    def disconnect(self):
        self.__client.close()

    def get_client(self):
        return self.__client
