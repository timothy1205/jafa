from typing import Optional
from backend.data.databases.DatabaseManager import DatabaseManager
from backend.data.databases.AbstractDatabase import AbstractDatabase


class DataManager:
    def __init__(self, database: Optional[AbstractDatabase] = None):
        if database is None:
            self.database = DatabaseManager().get_instance()
        else:
            self.database = database
