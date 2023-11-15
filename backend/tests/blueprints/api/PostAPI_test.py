import unittest

from backend.app import create_app
from backend.blueprints.api.PostAPI import PostAPI
from backend.data.managers.PostMananger import (
    InvalidPostBody,
    InvalidPostTag,
    InvalidPostTitle,
    NoPostFoundError,
    PostAlreadyLockedError,
    PostManager,
    PostNotLockedError,
    TagLimitExceeded,
)
from backend.data.managers.SubForumManager import NoSubForumFoundError
from backend.data.managers.VoteManager import (
    InvalidContent,
    InvalidContentType,
    NoVoteFoundError,
    VoteManager,
)
from backend.data.models.PostModel import Post
from backend.data.models.VoteModel import ContentType, Vote
from backend.tests.blueprints import (
    TestManagerFactory,
    blueprint_test_fail,
    blueprint_test_raise,
    blueprint_test_success,
)
from backend.utils import RolePermissionError


def create_post(client, subforum, title, body):
    return client.post(
        CREATE_ENDPOINT, data=dict(subforum=subforum, title=title, body=body)
    )


class TestPostManager(PostManager):
    def get_post(self, post_id: str) -> Post:
        pass

    def create_post(
        self,
        op: str,
        subforum: str,
        title: str,
        body: str,
        media: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> bool:  # NOSONAR
        pass

    def edit_post(
        self,
        username: str,
        post_id: str,
        title: str,
        body: str,
        media: list[str] | None = None,
        tags: list[str] | None = None,
    ):  # NOSONAR
        pass

    def delete_post(self, username: str, post_id: str) -> bool:  # NOSONAR
        pass

    def lock_post(self, username: str, post_id: str) -> bool:  # NOSONAR
        pass

    def unlock_post(self, username: str, post_id: str) -> bool:  # NOSONAR
        pass

    def add_like(
        self, post_id: str, is_like: bool, positive: bool = True
    ) -> bool:  # NOSONAR
        pass

    def get_post_list(
        self, subforum: str | None = None, page: int = 0, page_limit=None
    ) -> list[Post]:  # NOSONAR
        pass


class TestVoteManager(VoteManager):
    def get_vote(
        self, username: str, content_id: str, content_type: ContentType
    ) -> Vote:  # NOSONAR
        pass

    def add_vote(
        self,
        username: str,
        content_id: str,
        content_type: ContentType,
        is_like: bool,
    ):  # NOSONAR
        pass

    def remove_vote(
        self, username: str, content_id: str, content_type: ContentType
    ):  # NOSONAR
        pass

    def clear_votes_by_id(self, content_id: str):  # NOSONAR
        pass


class PostEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()

        self.test_manager_factory = TestManagerFactory()

        self.post_manager = TestPostManager()
        self.test_manager_factory.create_post_manager = lambda: self.post_manager

        self.vote_manager = TestVoteManager()
        self.test_manager_factory.create_vote_manager = lambda: self.vote_manager

        self.post_api = PostAPI(manager_factory=self.test_manager_factory)

    def test_create(self):
        run = self.post_api.create
        request_data = dict(subforum="", title="", body="")
        method = "create_post"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Post created",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Could not create",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            [
                InvalidPostTitle,
                InvalidPostBody,
                InvalidPostTag,
                TagLimitExceeded,
                NoSubForumFoundError,
            ],
        )

    def test_delete(self):
        run = self.post_api.delete
        request_data = dict(post_id="")
        method = "delete_post"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Post deleted",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Could not delete",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            [RolePermissionError, NoPostFoundError],
        )

    def test_edit(self):
        run = self.post_api.edit
        request_data = dict(post_id="", title="", body="")
        method = "edit_post"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Post updated",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Could not update post",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            [
                InvalidPostTitle,
                InvalidPostBody,
                InvalidPostTag,
                TagLimitExceeded,
                NoPostFoundError,
                RolePermissionError,
            ],
        )

    def test_lock(self):
        run = self.post_api.lock
        request_data = dict(post_id="")
        method = "lock_post"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Post locked",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Could not lock post",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            [NoPostFoundError, PostAlreadyLockedError, RolePermissionError],
        )

    def test_unlock(self):
        run = self.post_api.unlock
        request_data = dict(post_id="")
        method = "unlock_post"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Post unlocked",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            "Could not unlock post",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.post_manager,
            method,
            [NoPostFoundError, PostNotLockedError, RolePermissionError],
        )

    def test_vote(self):
        run = self.post_api.vote
        request_data = dict(post_id="", is_like="")
        method = "add_vote"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            "Post vote acknowledged",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            "Could not add post vote",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            [InvalidContentType, InvalidContent],
        )

    def test_unvote(self):
        run = self.post_api.unvote
        request_data = dict(post_id="")
        method = "remove_vote"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            "Post vote removed",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            "Could not remove post vote",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.vote_manager,
            method,
            [InvalidContentType, InvalidContent, NoVoteFoundError],
        )
