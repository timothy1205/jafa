from flask import Flask
from backend.databases.DatabaseManager import DatabaseManager


def create_app():
    app = Flask(__name__)

    # Register blueprint endpoints
    from backend.blueprints import api
    app.register_blueprint(api.blueprint)

    # Connect to database
    database = DatabaseManager.get_instance()
    database.connect("mongo")  # TODO: Use config option
    database.setup()

    return app
