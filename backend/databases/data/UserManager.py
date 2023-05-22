import re
from bcrypt import checkpw, hashpw, gensalt
from backend.databases.DatabaseManager import DatabaseManager
from backend.databases.data.DataManager import DataManager

USERS_LOCATION = "users"
PASSWORD_LENGTH = 8


class UsernameExistsError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserManager(DataManager):
    def __init__(self):
        self.__database = DatabaseManager.get_instance()

    def __get_user(self, username):
        user = self.__database.get(USERS_LOCATION, {"username": username})
        return user

    def __get_password_hash(self, username):
        user = self.__get_user(username)
        if user is None:
            return None

        return user["password"]

    def __valid_password(self, password: str):
        if len(password) < PASSWORD_LENGTH:
            return False
        if re.search('[0-9]', password) is None:
            return False
        if re.search('[A-Z]', password) is None:
            return False
        if re.search('[a-z]', password) is None:
            return False

        return True

    def check_password(self, username: str, password: str) -> bool:
        """Check if a given password corresponds to the saved hash

        :returns: True if password is valid. False if the user does not exist or the password is invalid
        """
        hashed_password = self.__get_password_hash(username)
        if hashed_password is None:
            return False

        return checkpw(password.encode("utf-8"), hashed_password)

    def create_user(self, username: str, password: str) -> bool:
        """Create a user inside the database if the username doesn't already exist

        :returns: True if successfull, false otherwise.
        :raises UsernameExistsError: Username already in database
        :raises Invali: Username already in database
        """
        if self.__get_user(username) is not None:
            raise UsernameExistsError("Username taken")

        if not self.__valid_password(password):
            raise InvalidPasswordError(
                f"Password must contain a lower/uppercase letter, number, and be at least {PASSWORD_LENGTH} characters")

        hashed_password = hashpw(
            password.encode("utf-8"), gensalt())
        return self.__database.create(
            USERS_LOCATION, {"username": username, "password": hashed_password})
