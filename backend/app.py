from secrets import token_hex

from flask import Flask
from flask_cors import CORS

from backend.data.databases.DatabaseFactory import DatabaseFactory
from backend.JafaConfig import JafaConfig


def create_app():
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    config = JafaConfig()

    CORS(app, origins=config.cors_origins, supports_credentials=True)

    # Register blueprint endpoints
    from backend.blueprints.route_manager import route_manager
    from backend.blueprints.api_manager import api_manager

    app.register_blueprint(route_manager.get_blueprint())
    app.register_blueprint(api_manager.get_blueprint())

    # Register index
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
