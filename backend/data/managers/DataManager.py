from flask import g
from typing import Optional, Type
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.ModelFactory import ModelFactory


class DataManager:
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        if model_factory is not None:
            self.model_factory = model_factory
        elif hasattr(g, "injected_model_factory"):
            # Allow for injecting a custom factory during testing
            self.model_factory = g.injected_model_factory
        else:
            self.model_factory = ModelFactory
