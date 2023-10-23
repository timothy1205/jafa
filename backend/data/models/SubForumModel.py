from abc import ABC, abstractmethod
from datetime import date
from typing import TypedDict

from backend.data.models.Model import Model


class SubForum(TypedDict):
    """Subforum data."""

    creator: str
    """Creator of a subforum."""
    title: str
    """Unique title of a subforum."""
    description: str
    """Descripton of a subforum."""
    creation_date: date
    """Creation date of a subforum."""


class SubForumModel(ABC, Model):
    @abstractmethod
    def create_subforum(self, data: SubForum) -> bool:
        """Create a subforum entry in the database.

        :param data: Subforum data.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_subforum(self, title: str) -> bool:
        """Delete a subforum entry in the database with a given title.

        :param data: Subforum data.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def edit_subforum(self, title: str, description: str) -> bool:
        """Edit a subforum's description in the database.

        :param title: Subforum to edit.
        :param description: New subforum description.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_subforum_by_title(self, title: str) -> SubForum | None:
        """Return a subforum with a given title, if any.

        :param title: Title to search for.

        :return: SubForum or None if `title` matches no exising titles.
        """

        raise NotImplementedError()
