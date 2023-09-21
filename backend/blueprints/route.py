import os.path
from glob import glob
from importlib import import_module

from flask import Blueprint, g, request, session

ROUTE_NAME = "route"
ROUTE_PATH = f"/{ROUTE_NAME}"

blueprint = Blueprint(ROUTE_NAME, __name__, url_prefix=ROUTE_PATH)

FILE_BLACKLIST = set(["__init__"])

# Find route blueprins
python_files = map(
    lambda path: os.path.basename(path).rstrip(".py"),
    glob(os.path.join(os.path.dirname(__file__), "routes", "*.py")),
)
blueprint_files = filter(lambda file: file not in FILE_BLACKLIST, python_files)

# Register route blueprints
for file in blueprint_files:
    module = import_module("backend.blueprints.routes." + file)
    blueprint.register_blueprint(module.blueprint)
