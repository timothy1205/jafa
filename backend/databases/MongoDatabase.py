from typing import Optional
from pymongo import MongoClient
from backend.databases.AbstractDatabase import AbstractDatabase


class MongoDatabase(AbstractDatabase):
    def __init__(self):
        self.__client = None
        self.__db = None

    def connect(self, hostname: str, port=27017, username=None, password=None):
        if username is None or password is None:
            self.__client = MongoClient(f"mongodb://{hostname}:{port}")
        else:
            self.__client = MongoClient(
                f"mongodb://{username}:{password}@{hostname}:{port}")

        self.__db = self.__client.jafa

    def setup(self):
        """Apply indexes"""
        self.__db["users"].create_index("username", unique=True)

    def disconnect(self):
        self.__client.close()

    def create(self, location: str, data: dict):
        collection = self.__db[location]
        result = collection.insert_one(data)
        return result.acknowledged

    def get(self, location: str, query: dict) -> Optional[dict]:
        colleciton = self.__db[location]
        result = colleciton.find_one(query, {"_id": False})
        return result

    def update(self, location: str, query: dict, data: dict) -> bool:
        collection = self.__db[location]
        result = collection.update_one(query, {"$set": data})
        return result.modified_count != 0

    def delete(self, location: str, query: dict) -> bool:
        collection = self.__db[location]
        result = collection.delete_one(query)
        return result.deleted_count != 0
