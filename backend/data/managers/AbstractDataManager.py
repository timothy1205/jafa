from abc import ABC
from typing import Type

from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.ModelFactory import ModelFactory


class AbstractDataManager(ABC):
    """Abstract DataManager class.

    :param: model_factory: The backend.data.models.AbstractModelFactory to use.
    A value of None will create a backend.data.models.ModelFactory object.
    """

    def __init__(self, model_factory: Type[AbstractModelFactory] | None = None):
        if model_factory is None:
            self.model_factory = ModelFactory()
        else:
            self.model_factory = model_factory
