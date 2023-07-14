from datetime import datetime
from typing import Optional, Type

from backend.data.managers.DataManager import DataManager
from backend.data.managers.VoteManager import VoteManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.PostModel import Post
from backend.utils import RolePermissionError

TITLE_MIN = 3
TITLE_MAX = 40
BODY_MIN = 5
BODY_MAX = 40000
TAG_MAX = 15
TAGS_LIMIT = 10
MEDIA_LIMIT = 10


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


class PostManager(DataManager):
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        super().__init__(model_factory)

    def __raise_or_return(self, post):
        if post is None:
            raise NoPostFoundError("A post with that ID does not exist")

        return post

    def __process_title(self, title: str):
        title = title.strip()

        if not (TITLE_MIN <= len(title) <= TITLE_MAX):
            raise InvalidPostTitle(
                f"Post title must be between [{TITLE_MIN}-{TITLE_MAX}] (inclusive) characters"
            )

        return title

    def __process_body(self, body: str):
        body = body.strip()
        if not (BODY_MIN <= len(body) <= BODY_MAX):
            raise InvalidPostBody(
                f"Post body must be between [{BODY_MIN}-{BODY_MAX}] (inclusive) characters"
            )

        return body

    def __process_tags(self, tags: Optional[list[str]]):
        if tags is None:
            return

        if len(tags) > TAGS_LIMIT:
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
        media: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
    ):
        """Create a post on behalf of a user to specified subforum

        :returns: True if successful, false otherwise.
        :raises InvalidPostTitle:
        :raises InvalidPostBody:
        :raises InvalidPostTag:
        :raises TagLimitExceeded:
        :raises NoTitleFoundError:
        """
        post_model = self.model_factory.create_post_model()
        subforum_manager = SubForumManager()

        # Throw NoTitleFoundError if invalid subforum
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
        media: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
    ):
        """Edit a post on behalf of a user

        :returns: True if successful, false otherwise.
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

        :returns: True if successfull, false otherwise.
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

        :returns: True if successfull, false otherwise.
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

        :returns: True if successfull, false otherwise.
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

    def add_likes(self, post_id: str, is_like: bool, amount: int) -> bool:
        """Add amount to a post's like/dislike count. Use negatives for subtracting

        :raises NoPostFoundError:
        """
        post_model = self.model_factory.create_post_model()
        post = self.get_post(post_id)

        likes = post["likes"]
        dislikes = post["dislikes"]

        if is_like:
            likes += amount
        else:
            dislikes += amount

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
        post_model = self.model_factory.create_post_model()

        return post_model.get_by_post_id(post_id) is not None
