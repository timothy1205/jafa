from flask import Blueprint
from backend.blueprints import user

API_NAME = "api"
API_PATH = f"/{API_NAME}"

blueprint = Blueprint(API_NAME, __name__, url_prefix=API_PATH)

# Register sub blueprints
blueprint.register_blueprint(user.blueprint)


@blueprint.route("/")
def index():
    return "Jafa is running!"
