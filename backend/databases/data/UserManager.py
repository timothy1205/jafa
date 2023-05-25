import re
from bcrypt import checkpw, hashpw, gensalt
from backend.databases.DatabaseManager import DatabaseManager
from backend.databases.data.DataManager import DataManager

USERS_LOCATION = "users"
PASSWORD_MIN = 8
PASSWORD_MAX = 256
USERNAME_MIN = 3
USERNAME_MAX = 40


class UsernameExistsError(Exception):
    pass


class InvalidUsernameError(Exception):
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

    def __valid_username(self, username: str):
        if not (USERNAME_MIN <= len(username) <= USERNAME_MAX):
            return False

        return True

    def __valid_password(self, password: str):
        if not (PASSWORD_MIN <= len(password) <= PASSWORD_MAX):
            return False
        if re.search('[0-9]', password) is None:
            return False
        if re.search('[A-Z]', password) is None:
            return False
        if re.search('[a-z]', password) is None:
            return False

        return True

    def check_password(self, username: str, password: str) -> tuple[bool, dict]:
        """Check if a given password corresponds to the saved hash

        :returns: Tuple[bool: password_is_valid, dict: user]
        """
        user = self.__get_user(username)
        if user is None:
            return False, None

        hashed_password = user["password"]
        return checkpw(password.encode("utf-8"), hashed_password), user

    def create_user(self, username: str, password: str) -> bool:
        """Create a user inside the database if the username doesn't already exist

        :returns: True if successfull, false otherwise.
        :raises UsernameExistsError: Username already in database
        :raises InvalidUsernameError: 
        :raises InvalidPasswordError: 
        """
        if not self.__valid_username(username):
            raise InvalidUsernameError(
                f"Username must be [{USERNAME_MIN}-{USERNAME_MAX}] characters")

        if self.__get_user(username) is not None:
            raise UsernameExistsError("Username taken")

        if not self.__valid_password(password):
            raise InvalidPasswordError(
                f"Password must contain a lower/uppercase letter, number, and be [{PASSWORD_MIN}-{PASSWORD_MAX}] characters")

        hashed_password = hashpw(
            password.encode("utf-8"), gensalt())
        return self.__database.create(
            USERS_LOCATION, {"username": username, "password": hashed_password})
