from glob import glob
import os.path
from importlib import import_module
from backend.JafaConfig import JafaConfig
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.UserModel import UserModel
from backend.data.models.SubForumModel import SubForumModel


class ModelFactory(AbstractModelFactory):
    _associations = None

    @staticmethod
    def __setup_associations():
        FILE_BLACKLIST = ["__init__",
                          "AbstractModelFactory", "ModelFactory", "Model"]
        ModelFactory._associations = {}
        python_files = glob(os.path.join(os.path.dirname(__file__), "**/*.py"))

        for path in python_files:
            base = os.path.basename(path).removesuffix(".py")
            if base in FILE_BLACKLIST:
                continue

            ModelFactory._associations[base.lower()] = base

    @staticmethod
    def __import_model(model_type):
        if ModelFactory._associations is None:
            ModelFactory.__setup_associations()

        database = JafaConfig().database_type
        path = ModelFactory._associations[database+model_type+"model"]
        module = import_module(f"backend.data.models.{database}.{path}")
        return getattr(module, path)

    @staticmethod
    def create_user_model() -> UserModel:
        model = ModelFactory.__import_model("user")
        return model()

    @staticmethod
    def create_subforum_model() -> SubForumModel:
        model = ModelFactory.__import_model("subforum")
        return model()
