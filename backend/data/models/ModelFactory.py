import os.path
from glob import glob
from importlib import import_module

from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.PostModel import PostModel
from backend.data.models.SubForumModel import SubForumModel
from backend.data.models.UserModel import UserModel
from backend.data.models.VoteModel import VoteModel
from backend.JafaConfigClass import jafa_config


class ModelFactory(AbstractModelFactory):
    _associations = None

    @staticmethod
    def __setup_associations():
        """Organize filenames of models into a dictionary.

        Key: File basename converted to lowercase.
        Value: Original file basename.
        """
        FILE_BLACKLIST = ["__init__", "AbstractModelFactory", "ModelFactory", "Model"]
        ModelFactory._associations = {}
        python_files = glob(os.path.join(os.path.dirname(__file__), "**/*.py"))

        for path in python_files:
            base = os.path.basename(path).removesuffix(".py")
            if base in FILE_BLACKLIST:
                continue

            ModelFactory._associations[base.lower()] = base

    @staticmethod
    def __import_model(model_type):
        """Dynamically import a model based on the database type and model type."""
        if ModelFactory._associations is None:
            ModelFactory.__setup_associations()

        database = jafa_config.database_type
        path = ModelFactory._associations[database + model_type + "model"]
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

    @staticmethod
    def create_vote_model() -> VoteModel:
        model = ModelFactory.__import_model("vote")
        return model()

    @staticmethod
    def create_post_model() -> PostModel:
        model = ModelFactory.__import_model("post")
        return model()
