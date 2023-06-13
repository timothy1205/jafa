from typing import Optional
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.ModelFactory import ModelFactory


class DataManager:
    def __init__(self, model_factory: Optional[AbstractModelFactory] = None):
        if model_factory is None:
            self.model_factory = ModelFactory
        else:
            self.model_factory = model_factory
