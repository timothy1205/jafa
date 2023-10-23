from abc import ABC, abstractmethod
from datetime import date
from typing import TypedDict

from backend.data.models.Model import Model


class BasePost(TypedDict):
    """Generic post data."""

    op: str
    """Creator of a post."""
    title: str
    """Title of a post."""
    body: str
    """Body of a post."""
    media: list[str] | None
    """Media within a post."""
    tags: list[str] | None
    """Tags associated with a post."""
    modified_date: date | None
    """Last time a post was modified."""
    likes: int
    """Current amount of likes a post has."""
    dislikes: int
    """Current amount of dislikes a post has."""


class CreatePost(BasePost):
    """Additonal data required for creating a post."""

    subforum: str
    """Subforum a post belongs to."""

    creation_date: date
    """The date of when a post was created."""
    locked: bool
    """If a post is currently locked."""


class Post(CreatePost):
    """Complete post data when retreiving from the database."""

    post_id: str
    """Unique ID of a post."""


class PostModel(ABC, Model):
    @abstractmethod
    def create_post(self, data: CreatePost) -> bool:
        """Create a post inside the database.

        :param data: Data to create post with.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_post_id(self, post_id: str) -> Post | None:
        """Return a post from the database associated with a given id, if any.

        :param post_id: Unique ID of post to get.

        :return: Post or None if no post found.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_by_post_id(self, post_id: str) -> bool:
        """Delete a post from the database associated with a given id, if any.

        :param post_id: Unique ID of post.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_posts(self, username: str) -> bool:
        """Clear all posts created by `username`.

        :param username: Username.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def edit_post(self, post_id: str, data: BasePost) -> bool:
        """Modify post data to the contents of `data`.

        :param post_id: Unique ID of post to edit.
        :param data: Data to edit post to.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def lock_post(self, post_id: str) -> bool:
        """Lock a post associated with a given id.

        :param post_id: Unique ID of post to lock.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def unlock_post(self, post_id: str) -> bool:
        """Unlock a post associated with a given id.

        :param post_id: Unique ID of post to unlock.

        :return: True if successful.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_posts(
        self, limit: int, skip: int, subforum: str | None = None
    ) -> list[Post]:
        """Return a list of posts within the given parameters.
        :param limit: Max amount of posts to return.
        :param skip: Amount of posts to skip before grabbing.
        :param subforum: Subforum to filter posts from. A value of None indicates that all subforums should be used.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_count(self, subforum: str | None = None) -> int:
        """Return the amount of existing posts.

        :param subforum: Subforum to filter posts from. A value of None indicates that all subforums should be used.
        """
        raise NotImplementedError()
