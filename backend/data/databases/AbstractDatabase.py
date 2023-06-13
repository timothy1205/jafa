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
    def get_client(self):
        raise NotImplementedError
