from flask import Blueprint
from ..constants import API_NAME, API_PATH, API_GREETING

blueprint = Blueprint(API_NAME, __name__, url_prefix=API_PATH)
# Register sub blueprints

@blueprint.route("/")
def index():
    return API_GREETING