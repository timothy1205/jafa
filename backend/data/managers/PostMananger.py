from datetime import datetime
from typing import Type

from backend.data.managers.AbstractDataManager import AbstractDataManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.data.managers.VoteManager import VoteManager
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.PostModel import Post
from backend.utils import RolePermissionError

TITLE_MIN = 3
"""Minimum title character limit."""
TITLE_MAX = 40
"""Maximum title character limit."""
BODY_MIN = 5
"""Minimum body character limit."""
BODY_MAX = 40000
"""Maximum body character limit."""
TAG_MAX = 15
"""Maximum tag character limit."""
TAGS_LIMIT = 10
"""Maximum tag count."""
MEDIA_LIMIT = 10
"""Maximum media count."""
PAGE_LIMIT = 20
"""Maximum page count."""


class InvalidPostTitle(Exception):
    pass


class InvalidPostBody(Exception):
    pass


class InvalidPostTag(Exception):
    pass


class TagLimitExceeded(Exception):
    pass


class NoPostFoundError(Exception):
    pass


class PostAlreadyLockedError(Exception):
    pass


class PostNotLockedError(Exception):
    pass


class InvalidPageError(Exception):
    pass


class PostManager(AbstractDataManager):
    """Handle post related functionality."""

    def __init__(self, model_factory: Type[AbstractModelFactory] | None = None):
        super().__init__(model_factory)

    def __raise_or_return(self, post):
        if post is None:
            raise NoPostFoundError("A post with that ID does not exist")

        return post

    def __process_title(self, title: str):
        """Strip title and verify character limits.

        :raises InvalidPostTitle:
        """
        title = title.strip()

        if not (TITLE_MIN <= len(title) <= TITLE_MAX):
            raise InvalidPostTitle(
                f"Post title must be between [{TITLE_MIN}-{TITLE_MAX}] (inclusive) characters"
            )

        return title

    def __process_body(self, body: str):
        """Strip body and verify character limits.

        :raises InvalidPostBody:
        """
        body = body.strip()
        if not (BODY_MIN <= len(body) <= BODY_MAX):
            raise InvalidPostBody(
                f"Post body must be between [{BODY_MIN}-{BODY_MAX}] (inclusive) characters"
            )

        return body

    def __process_tags(self, tags: list[str] | None):
        """Strip tags and verify character limits.

        :raises TagLimitExceeded:
        :raises InvalidPostTag:
        """
        if tags is None:
            return

        if len(tags) == 0:
            return None
        elif len(tags) > TAGS_LIMIT:
            raise TagLimitExceeded(f"Exceeded tag limit of {TAGS_LIMIT}")

        def __check_tag(tag: str):
            tag = tag.strip()
            if tag == "":
                raise InvalidPostTag("Tag cannot be empty")
            elif len(tag) > TAG_MAX:
                raise InvalidPostTag(f"Tag cannot exceed {TAG_MAX} characters")

            return tag

        return list(map(__check_tag, tags))

    def get_post(self, post_id: str) -> Post:
        """Return post with specified id

        :raises NoPostFoundError:
        """
        post_model = self.model_factory.create_post_model()

        return self.__raise_or_return(post_model.get_by_post_id(post_id))

    def create_post(
        self,
        op: str,
        subforum: str,
        title: str,
        body: str,
        media: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> bool:
        """Create a post on behalf of a user to specified subforum

        :return: True if successful, false otherwise.
        :raises InvalidPostTitle:
        :raises InvalidPostBody:
        :raises InvalidPostTag:
        :raises TagLimitExceeded:
        :raises NoSubForumFoundError:
        """
        post_model = self.model_factory.create_post_model()
        subforum_manager = SubForumManager(self.model_factory)

        # Throw NoSubForumFoundError if invalid subforum
        subforum_manager.get_subforum(subforum)

        title = self.__process_title(title)
        body = self.__process_body(body)
        tags = self.__process_tags(tags)

        now = datetime.now()
        return post_model.create_post(
            dict(
                op=op,
                subforum=subforum,
                title=self.__process_title(title),
                body=self.__process_body(body),
                media=media,
                tags=self.__process_tags(tags),
                likes=0,
                dislikes=0,
                locked=False,
                creation_date=now,
                modified_date=now,
            )
        )

    def edit_post(
        self,
        username: str,
        post_id: str,
        title: str,
        body: str,
        media: list[str] | None = None,
        tags: list[str] | None = None,
    ):
        """Edit a post on behalf of a user

        :return: True if successful, false otherwise.
        :raises NoPostFoundError:
        :raises InvalidPostTitle:
        :raises InvalidPostBody:
        :raises InvalidPostTag:
        :raises TagLimitExceeded:
        :raises RolePermissionError:
        """
        post_model = self.model_factory.create_post_model()
        post = self.get_post(post_id)

        op = post["op"]

        if op != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        title = self.__process_title(title)
        body = self.__process_body(body)
        tags = self.__process_tags(tags)

        return post_model.edit_post(
            post_id,
            dict(
                op=op,
                title=title,
                body=body,
                media=media,
                tags=tags,
                modified_date=datetime.now(),
                likes=post["likes"],
                dislikes=post["dislikes"],
            ),
        )

    def delete_post(self, username: str, post_id: str) -> bool:
        """Delete a post of a given ID on behalf of a user as permitted

        :return: True if successfull, false otherwise.
        :raises RolePermissionError:
        :raises NoPostFoundError:
        """
        post_model = self.model_factory.create_post_model()
        vote_manager = VoteManager(self.model_factory)
        post = self.get_post(post_id)

        op = post["op"]

        if op != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        # Also clear associated votes
        vote_manager.clear_votes_by_id(post_id)

        return post_model.delete_by_post_id(post_id)

    def lock_post(self, username: str, post_id: str) -> bool:
        """Mark a post as locked on behalf of a user as permitted

        :return: True if successfull, false otherwise.
        :raises NoPostFoundError:
        :raises PostAlreadyLockedError:
        :raises RolePermissionError:
        """
        post_model = self.model_factory.create_post_model()
        post = self.get_post(post_id)

        locked = post["locked"]
        op = post["op"]

        if locked:
            raise PostAlreadyLockedError("Post already marked as locked")

        if op != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        return post_model.lock_post(post_id)

    def unlock_post(self, username: str, post_id: str) -> bool:
        """Mark a post as unlocked on behalf of a user as permitted

        :return: True if successfull, false otherwise.
        :raises NoPostFoundError:
        :raises PostNotLockedError:
        :raises RolePermissionError:
        """
        post_model = self.model_factory.create_post_model()
        post = self.get_post(post_id)

        locked = post["locked"]
        op = post["op"]

        if not locked:
            raise PostNotLockedError("Post already marked as unlocked")

        if op != username:
            # TODO: Allow moderators to bypass
            raise RolePermissionError()

        return post_model.unlock_post(post_id)

    def add_like(self, post_id: str, is_like: bool, positive: bool = True) -> bool:
        """Add to a post's like/dislike count. positive indicates whether it should be 1 or -1

        :raises NoPostFoundError:
        """
        post_model = self.model_factory.create_post_model()
        post = self.get_post(post_id)

        likes = post["likes"]
        dislikes = post["dislikes"]

        amount = 1 if positive else -1

        # Add amount, ensure values never go below 0
        if is_like:
            likes = max(likes + amount, 0)
        else:
            dislikes = max(dislikes + amount, 0)

        return post_model.edit_post(
            post_id,
            dict(
                op=post["op"],
                title=post["title"],
                body=post["body"],
                media=post["media"],
                tags=post["tags"],
                modified_date=post["modified_date"],
                likes=likes,
                dislikes=dislikes,
            ),
        )

    def post_exists(self, post_id: str) -> bool:
        """Ensure a posts exists

        :return: True if given post exists, false otherwise.
        """
        post_model = self.model_factory.create_post_model()

        return post_model.get_by_post_id(post_id) is not None

    def get_post_list(
        self, subforum: str | None = None, page: int = 0, page_limit=None
    ) -> list[Post]:
        """Returns a list of posts

        :raises InvalidPageError"
        """
        post_model = self.model_factory.create_post_model()

        if page_limit is None:
            page_limit = PAGE_LIMIT
        try:
            return post_model.get_posts(page_limit, page_limit * page, subforum)
        except OverflowError:
            # Reraise OverflowErrors into something neater
            raise InvalidPageError("Invalid page number")
