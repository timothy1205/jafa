import os


class JafaConfig:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        """Load config values from environmental variables"""
        if hasattr(self, "loaded"):
            return

        self.database_type = os.getenv("DATABASE_TYPE")
        self.database_host = os.getenv("DATABASE_HOST")
        self.database_port = os.getenv("DATABASE_PORT")
        self.database_username = os.getenv("DATABASE_USERNAME")
        self.database_password = os.getenv("DATABASE_PASSWORD")
        self.cors_origins = os.getenv("WHITELISTED_ORIGINS", "").split(",")
        self.loaded = True
