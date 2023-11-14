import re
from base64 import b64encode
from datetime import datetime
from hashlib import sha256
from typing import Optional, Type

from bcrypt import checkpw, gensalt, hashpw

from backend.data.models.UserModel import User
from backend.data.managers.AbstractDataManager import AbstractDataManager
from backend.data.models.AbstractModelFactory import AbstractModelFactory

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


class UserManager(AbstractDataManager):
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        super().__init__(model_factory)

    def __pre_hash_password(self, password):
        encoded = password.encode("utf-8")
        return b64encode(sha256(encoded).digest())

    def __valid_username(self, username: str):
        if not (USERNAME_MIN <= len(username) <= USERNAME_MAX):
            return False
        if not username.isalnum():
            return False

        return True

    def __valid_password(self, password: str):
        if not (PASSWORD_MIN <= len(password) <= PASSWORD_MAX):
            return False
        if re.search("[\d]", password) is None:
            return False
        if re.search("[A-Z]", password) is None:
            return False
        if re.search("[a-z]", password) is None:
            return False

        return True

    def user_exists(self, username: str) -> bool:
        """Check database for username

        :returns: True if the username exists, false otherwise.
        """
        user_model = self.model_factory.create_user_model()
        return user_model.get_by_username(username) is not None

    def check_password(self, username: str, password: str) -> tuple[bool, User]:
        """Check if a given password corresponds to the saved hash

        :returns: Tuple[bool: password_is_valid, dict: user]
        """
        user_model = self.model_factory.create_user_model()
        user = user_model.get_by_username(username)
        if user is None:
            return False, None

        hashed_password = user["password"]
        if not checkpw(self.__pre_hash_password(password), hashed_password):
            return False, None

        return True, user

    def create_user(self, username: str, password: str) -> User | None:
        """Create a user inside the database if the username doesn't already exist

        :returns: True if successfull, false otherwise.
        :raises UsernameExistsError: Username already in database
        :raises InvalidUsernameError:
        :raises InvalidPasswordError:
        """
        user_model = self.model_factory.create_user_model()

        if not self.__valid_username(username):
            raise InvalidUsernameError(
                f"Username must be [{USERNAME_MIN}-{USERNAME_MAX}] characters and contain no special characters"
            )

        if self.user_exists(username):
            raise UsernameExistsError("Username taken")

        if not self.__valid_password(password):
            raise InvalidPasswordError(
                f"Password must contain a lower/uppercase letter, number, and be [{PASSWORD_MIN}-{PASSWORD_MAX}] characters"
            )

        hashed_password = hashpw(self.__pre_hash_password(password), gensalt())

        user: User = dict(
            username=username,
            password=hashed_password,
            registration_date=datetime.now(),
        )

        return user if user_model.create_user(user) else None
