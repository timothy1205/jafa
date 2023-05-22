from flask import Flask
from .constants import API_PATH

def create_app():
    app = Flask(__name__)

    # Register blueprint endpoints
    from .blueprints import api
    app.register_blueprint(api.blueprint)

    return app