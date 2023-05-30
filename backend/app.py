from flask import Flask
from secrets import token_hex
from backend.databases.DatabaseManager import DatabaseManager
from backend.JafaConfig import JafaConfig


def create_app():
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    config = JafaConfig()

    # Register blueprint endpoints
    from backend.blueprints import api
    app.register_blueprint(api.blueprint)

    # Connect to database
    database = DatabaseManager.get_instance()
    database.connect(config.database_host, config.database_port,
                     config.database_username, config.database_password)
    database.setup()

    return app
