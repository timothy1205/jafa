import os


class JafaConfigClass:
    """Class to load config values from environmental variables"""

    database_type: str | None
    database_host: str | None
    database_port: str | None
    database_username: str | None
    database_password: str | None
    cors_origins: list[str]

    def __init__(self):
        self.database_type: str | None = os.getenv("DATABASE_TYPE")
        """Database type"""
        self.database_host = os.getenv("DATABASE_HOST")
        """Database host"""
        self.database_port = os.getenv("DATABASE_PORT")
        """Database port"""
        self.database_username = os.getenv("DATABASE_USERNAME")
        """Database username"""
        self.database_password = os.getenv("DATABASE_PASSWORD")
        """Database password"""
        self.cors_origins = os.getenv("WHITELISTED_ORIGINS", "").split(",")
        """List of whitelisted CORS urls"""
        self.testing = False
        """Indicate we are running tests, should be overriden"""


jafa_config = JafaConfigClass()
