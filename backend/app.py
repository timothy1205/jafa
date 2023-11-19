from secrets import token_hex

from flask import Flask
from flask_cors import CORS

from backend.blueprints.APIBlueprintManager import APIBlueprintManager
from backend.blueprints.APIRouteManager import RouteBlueprintManager
from backend.data.databases.DatabaseFactory import DatabaseFactory
from backend.JafaConfigClass import jafa_config


def create_app() -> Flask:
    """Create Flask app for Jafa.

    :return: A customized instance of Flask"""
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    # Initialize CORS
    CORS(app, origins=jafa_config.cors_origins, supports_credentials=True)

    # Register blueprint endpoints
    app.register_blueprint(APIBlueprintManager().get_blueprint())
    app.register_blueprint(RouteBlueprintManager().get_blueprint())

    # Register index endpoint
    @app.route("/")
    def index():
        return "Jafa is running!"

    # Connect to database if we are not testing
    if not jafa_config.testing:
        database = DatabaseFactory.create_database(jafa_config.database_type)
        database.connect(
            jafa_config.database_host,
            jafa_config.database_port,
            jafa_config.database_username,
            jafa_config.database_password,
        )
        database.setup()

    return app
