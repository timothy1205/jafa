from backend.databases.DatabaseManager import DatabaseManager


class DataManager:
    def __init__(self, database=None):
        if database is None:
            self.__database = DatabaseManager().get_instance()
        else:
            self.__database = database
