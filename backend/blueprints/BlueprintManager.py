import os.path
from glob import glob

from flask import Blueprint
from backend.utils import make_blueprint
from importlib.util import spec_from_file_location, module_from_spec


class BlueprintManager:
    """Manage the importing of several child blueprints.
    Creates a base blueprint and imports all blueprints found at a given import_path.

    Populate file_blacklist with file names (without extensions) to ignore those files. __init__ is included automatically.
    """

    def __init__(
        self,
        name: str,
        import_name: str,
        import_path: str,
        url_prefix: str | None = None,
        file_blacklist: set[str] = None,
    ):
        self.__blueprint = make_blueprint(name, import_name, url_prefix)

        if file_blacklist is None:
            file_blacklist = set()

        # Always include __init__.py
        file_blacklist.add("__init__")

        # Derive blueprints from python files

        mapped_files = map(
            lambda path: (os.path.basename(path).rstrip(".py"), path),
            glob(os.path.join(import_path, "*.py")),
        )

        # Filter out blacklisted files
        filtered_files = filter(
            lambda base_path: base_path[0] not in file_blacklist, mapped_files
        )

        # Register sub blueprints
        for base, file in filtered_files:
            spec = spec_from_file_location(base, file)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "blueprint") and type(module.blueprint) is Blueprint:
                self.__blueprint.register_blueprint(module.blueprint)
            else:
                # TODO: Log warning
                pass

    def get_blueprint(self):
        """Return inner blueprint object"""
        return self.__blueprint
