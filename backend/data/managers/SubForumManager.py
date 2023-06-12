from typing import Optional
import re
from bcrypt import checkpw, hashpw, gensalt
from hashlib import sha256
from base64 import b64encode
from backend.data.databases.DatabaseManager import DatabaseManager
from backend.data.databases.AbstractDatabase import AbstractDatabase
from backend.data.managers.DataManager import DataManager
from backend.utils import RolePermissionError

SUBFORUM_LOCATION = "subforums"
TITLE_MIN = 3
TITLE_MAX = 40
DESCRIPTION_MAX = 650


class TitleExistsError(Exception):
    pass


class NoTitleFoundError(Exception):
    pass


class InvalidTitleError(Exception):
    pass


class InvalidDescriptionError(Exception):
    pass


class UnchangedDescriptionError(Exception):
    pass


class SubForumManager(DataManager):
    def __init__(self, database: AbstractDatabase = None):
        super().__init__(database)

    def __get_subforum(self, title):
        subforum = self.database.get(SUBFORUM_LOCATION, {"title": title})
        return subforum

    def __get_subforum_or_raise(self, title):
        subforum = self.__get_subforum(title)
        if subforum is None:
            raise NoTitleFoundError(
                "A subforum with that title does not exist")

        return subforum

    def __valid_title(self, title):
        if not (TITLE_MIN <= len(title) <= TITLE_MAX):
            return False
        if re.match('^[a-zA-Z0-9]+(_*[a-zA-Z0-9]+)*$', title) is None:
            return False

        return True

    def __valid_description(self, description):
        if len(description) > DESCRIPTION_MAX:
            return False
        if description == "":
            return False

        return True

    def create_subforum(self, creator: str, title: str, description: str) -> bool:
        """Create a subforum inside the database if the title doesn't already exist

        :returns: True if successful, false otherwise.
        :raises TitleExistsError:
        :raises InvalidTitleError:
        :raises InvalidDescriptionError:
        """
        if not self.__valid_description(description):
            raise InvalidDescriptionError("Description cannot be empty")

        if self.__get_subforum(title) is not None:
            raise TitleExistsError("A subforum with that title already exists")

        if not self.__valid_title(title):
            raise InvalidTitleError(
                "Title may contain letters, numbers, and underscores. Underscores cannot be leading or trailing")

        return self.database.create(
            SUBFORUM_LOCATION, {"creator": creator, "title": title, "description": description})

    def delete_subforum(self, username: str, title: str) -> bool:
        """Delete a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoTitleFoundError:
        """
        subforum = self.__get_subforum_or_raise(title)

        if subforum["creator"] != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        return self.database.delete(SUBFORUM_LOCATION, {"title": title})

    def edit_subforum(self, username: str, title: str, description: str) -> bool:
        """Edit a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoTitleFoundError:
        :raises InvalidDescriptionError:
        """
        subforum = self.__get_subforum_or_raise(title)

        if not self.__valid_description(description):
            raise InvalidDescriptionError("Description cannot be empty")

        if subforum["creator"] != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        if subforum["description"] == description:
            raise UnchangedDescriptionError("There is nothing to update")

        return self.database.update(SUBFORUM_LOCATION, {"title": title}, {"description": description})
