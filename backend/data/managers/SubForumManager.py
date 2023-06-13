from typing import Optional, Type
import re
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.managers.DataManager import DataManager
from backend.utils import RolePermissionError

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
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        super().__init__(model_factory)

    def __raise_or_return(self, subforum):
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
        subforum_model = self.model_factory.create_subforum_model()

        if not self.__valid_description(description):
            raise InvalidDescriptionError("Description cannot be empty")

        if subforum_model.get_by_title(title) is not None:
            raise TitleExistsError("A subforum with that title already exists")

        if not self.__valid_title(title):
            raise InvalidTitleError(
                "Title may contain letters, numbers, and underscores. Underscores cannot be leading or trailing")

        return subforum_model.create_subforum(creator, title, description)

    def delete_subforum(self, username: str, title: str) -> bool:
        """Delete a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoTitleFoundError:
        """
        subforum_model = self.model_factory.create_subforum_model()
        subforum = self.__raise_or_return(subforum_model.get_by_title(title))

        if subforum["creator"] != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        return subforum_model.delete_subforum(title)

    def edit_subforum(self, username: str, title: str, description: str) -> bool:
        """Edit a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoTitleFoundError:
        :raises InvalidDescriptionError:
        """
        subforum_model = self.model_factory.create_subforum_model()
        subforum = self.__raise_or_return(subforum_model.get_by_title(title))

        if not self.__valid_description(description):
            raise InvalidDescriptionError("Description cannot be empty")

        if subforum["creator"] != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        if subforum["description"] == description:
            raise UnchangedDescriptionError("There is nothing to update")

        return subforum_model.edit_subforum(title, description)
