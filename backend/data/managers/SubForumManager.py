import re
from datetime import datetime
from typing import Optional, Type, TypedDict

from backend.data.managers.AbstractDataManager import AbstractDataManager
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.SubForumModel import SubForum
from backend.utils import RolePermissionError, ceil_division

TITLE_MIN = 3
TITLE_MAX = 40
DESCRIPTION_MAX = 650


class SubForumTitleExistsError(Exception):
    pass


class NoSubForumFoundError(Exception):
    pass


class InvalidSubForumTitle(Exception):
    pass


class InvalidSubForumDescription(Exception):
    pass


class SubForumInfoGeneric(TypedDict):
    post_count: int
    page_count: int
    current_page: int


class SubForumInfoSpecific(SubForumInfoGeneric, SubForum):
    pass


class SubForumManager(AbstractDataManager):
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        super().__init__(model_factory)

    def __raise_or_return(self, subforum):
        if subforum is None:
            raise NoSubForumFoundError("A subforum with that title does not exist")

        return subforum

    def __valid_title(self, title):
        if not (TITLE_MIN <= len(title) <= TITLE_MAX):
            return False
        if re.match("^[a-zA-Z0-9]+(_*[a-zA-Z0-9]+)*$", title) is None:
            return False

        return True

    def __valid_description(self, description):
        if len(description) > DESCRIPTION_MAX:
            return False
        if description == "":
            return False

        return True

    def get_subforum(self, title: str) -> SubForum:
        """Return a subforum with a given title

        :raises NoSubForumFoundError:
        """
        subforum_model = self.model_factory.create_subforum_model()

        return self.__raise_or_return(subforum_model.get_subforum_by_title(title))

    def create_subforum(self, creator: str, title: str, description: str) -> bool:
        """Create a subforum inside the database if the title doesn't already exist

        :returns: True if successful, false otherwise.
        :raises SubForumTitleExistsError:
        :raises InvalidSubForumTitle:
        :raises InvalidSubForumDescription:
        """
        subforum_model = self.model_factory.create_subforum_model()

        if not self.__valid_description(description):
            raise InvalidSubForumDescription("Description cannot be empty")

        if subforum_model.get_subforum_by_title(title) is not None:
            raise SubForumTitleExistsError("A subforum with that title already exists")

        if not self.__valid_title(title):
            raise InvalidSubForumTitle(
                "Title may contain letters, numbers, and underscores. Underscores cannot be leading or trailing"
            )

        return subforum_model.create_subforum(
            dict(
                creator=creator,
                title=title,
                description=description,
                creation_date=datetime.now(),
            )
        )

    def delete_subforum(self, username: str, title: str) -> bool:
        """Delete a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoSubForumFoundError:
        """
        subforum_model = self.model_factory.create_subforum_model()
        subforum = self.__raise_or_return(subforum_model.get_subforum_by_title(title))

        if subforum["creator"] != username:
            # TODO: Allow admins to bypass
            raise RolePermissionError()

        return subforum_model.delete_subforum(title)

    def edit_subforum(self, username: str, title: str, description: str) -> bool:
        """Edit a subforum on behalf of a user as permitted

        :returns: True if successful, false otherwise.
        :raises RolePermissionError:
        :raises NoSubForumFoundError:
        :raises InvalidSubForumDescription:
        """
        subforum_model = self.model_factory.create_subforum_model()
        subforum = self.get_subforum(title)

        if not self.__valid_description(description):
            raise InvalidSubForumDescription("Description cannot be empty")

        if subforum["creator"] != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        return subforum_model.edit_subforum(title, description)

    def get_subforum_info(
        self,
        title: str | None = None,
        current_page: int = 0,
        page_limit: int | None = None,
    ) -> SubForumInfoGeneric | SubForumInfoSpecific:
        """Returns a dict of info for a valid subforum or generic info if None

        :returns: SubForumInfoGeneric | SubForumInfoSpecific
        :raises NoSubForumFoundError:
        """

        if page_limit is None:
            from backend.data.managers.PostMananger import PAGE_LIMIT

            page_limit = PAGE_LIMIT

        post_model = self.model_factory.create_post_model()
        post_count = post_model.get_count(title)
        page_count = ceil_division(post_count, page_limit)
        subforum_info = dict(
            post_count=post_count, page_count=page_count, current_page=current_page
        )

        if title is None:
            return subforum_info

        subforum = self.get_subforum(title)

        return subforum | subforum_info
