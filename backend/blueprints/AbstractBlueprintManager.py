import os.path
from glob import glob

from flask import Blueprint
from backend.utils import make_blueprint


class AbstractBlueprintManager:
    """Manage the importing of several child blueprints."""

    def __init__(
        self,
        name: str,
        import_name: str,
        url_prefix: str | None = None,
    ):
        self.__blueprint = make_blueprint(name, import_name, url_prefix)

    def get_blueprint(self) -> Blueprint:
        """Return inner blueprint object"""
        return self.__blueprint
