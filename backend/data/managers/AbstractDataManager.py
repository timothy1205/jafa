from typing import Type

from flask import g

from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.ModelFactory import ModelFactory

from abc import ABC


class AbstractDataManager(ABC):
    """Abstract DataManager class.

    :param: model_factory: The backend.data.models.AbstractModelFactory to use.
    A value of None will attempt to the `injected_model_factory` value from the
    Flask `g` object, or simply create a backend.data.models.ModelFactory object.
    """

    def __init__(self, model_factory: Type[AbstractModelFactory] | None = None):
        if model_factory is not None:
            self.model_factory = model_factory
        elif hasattr(g, "injected_model_factory"):
            # Allow for injecting a custom factory during testing
            self.model_factory = g.injected_model_factory
        else:
            self.model_factory = ModelFactory()
