from flask import Flask
from secrets import token_hex
from backend.databases.DatabaseManager import DatabaseManager


def create_app():
    app = Flask(__name__)
    app.secret_key = token_hex(16)

    # Register blueprint endpoints
    from backend.blueprints import api
    app.register_blueprint(api.blueprint)

    # Connect to database
    database = DatabaseManager.get_instance()
    database.connect("mongo")  # TODO: Use config option
    database.setup()

    return app
