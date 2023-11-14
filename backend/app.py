from secrets import token_hex

from flask import Flask
from flask_cors import CORS

from backend.blueprints.APIBlueprintManager import APIBlueprintManager
from backend.blueprints.APIRouteManager import RouteBlueprintManager
from backend.data.databases.DatabaseFactory import DatabaseFactory
from backend.JafaConfig import JafaConfig


def create_app() -> Flask:
    """Create Flask app for Jafa.

    :return: A customized instance of Flask"""
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    # Load config
    config = JafaConfig()

    # Initialize CORS
    CORS(app, origins=config.cors_origins, supports_credentials=True)

    # Register blueprint endpoints
    app.register_blueprint(APIBlueprintManager().get_blueprint())
    app.register_blueprint(RouteBlueprintManager().get_blueprint())

    # Register index endpoint
    @app.route("/")
    def index():
        return "Jafa is running!"

    # Connect to database if we are not testing
    if config.database_type != "testing":
        database = DatabaseFactory.create_database(config.database_type)
        database.connect(
            config.database_host,
            config.database_port,
            config.database_username,
            config.database_password,
        )
        database.setup()

    return app
