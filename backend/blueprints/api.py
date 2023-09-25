import os.path
from glob import glob
from importlib import import_module

from backend.utils import make_blueprint

FILE_BLACKLIST = set(["__init__", "api"])

blueprint = make_blueprint("api", __name__)

# Derive blueprints from python files
python_files = map(
    lambda path: os.path.basename(path).rstrip(".py"),
    glob(os.path.join(os.path.dirname(__file__), "*.py")),
)
blueprint_files = filter(lambda file: file not in FILE_BLACKLIST, python_files)

# Register sub blueprints
for file in blueprint_files:
    module = import_module("backend.blueprints." + file)
    blueprint.register_blueprint(module.blueprint)


@blueprint.route("/")
def index():
    return "Jafa is running!"
