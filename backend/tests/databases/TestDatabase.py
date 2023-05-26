from typing import Optional
from backend.databases.AbstractDatabase import AbstractDatabase


class TestDatabase(AbstractDatabase):
    """Test database that implements AbstractDatabase for testing purposes"""

    def __init__(self):
        self.__db = {}

    def connect(self, hostname: str, port=None, username=None, password=None):
        pass  # Not needed

    def setup(self):
        pass  # Not needed

    def disconnect(self):
        pass  # Not needed

    def create(self, location: str, data: dict) -> bool:
        self.__db[location] = data
        return True

    def get(self, location: str, query: dict) -> Optional[dict]:
        return self.__db.get(location)

    def update(self, location: str, query: dict, data: dict):
        self.__db[location] |= data
        return True

    def delete(self, location: str, query: dict):
        del self.__db[location]

    def get_db(self):
        return self.__db
