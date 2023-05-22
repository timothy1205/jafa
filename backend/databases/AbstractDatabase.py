from abc import ABC, abstractmethod
from typing import Optional


class AbstractDatabase(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def connect(self, hostname: str, port=None, username=None, password=None):
        raise NotImplementedError

    @abstractmethod
    def setup(self):
        """Post-connect setup call.

        Optional implementation since some types of DBs don't require it.
        """
        pass

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, location: str, data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, location: str, query: dict) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def update(self, location: str, query: dict, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, location: str, query: dict):
        raise NotImplementedError
