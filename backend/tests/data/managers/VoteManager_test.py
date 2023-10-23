import unittest

import backend.data.managers.VoteManager as vm
from backend.data.models.VoteModel import BaseVote, Vote, VoteModel
from backend.tests import assertTimeInRange
from backend.tests.data.managers import TestModelFactory
from backend.utils import set_data_wrapper


class TestVoteModel(VoteModel):
    def add_vote(self, data: Vote) -> bool:  # NOSONAR
        pass

    def get_vote(self, data: BaseVote) -> Vote | None:  # NOSONAR
        pass

    def update_vote(self, data: Vote) -> bool:  # NOSONAR
        pass

    def remove_vote(self, data: BaseVote) -> bool:  # NOSONAR
        pass

    def clear_votes_by_username(self, username: str) -> bool:  # NOSONAR
        pass

    def clear_votes_by_id(self, content_id: str) -> bool:  # NOSONAR
        pass


class VoteManagerTestCase(unittest.TestCase):
    def setUp(self):
        from backend.tests.data.managers.PostManager_test import TestPostModel
        from backend.tests.data.managers.SubForumManager_test import TestSubForumModel

        self.post_model = TestPostModel()
        self.subforum_model = TestSubForumModel()
        self.vote_model = TestVoteModel()

        test_model_factory = TestModelFactory()
        test_model_factory.create_post_model = lambda: self.post_model
        test_model_factory.create_subforum_model = lambda: self.subforum_model
        test_model_factory.create_vote_model = lambda: self.vote_model
        self.vote_manager = vm.VoteManager(test_model_factory)
        self.data = {}

    def test_get_vote(self):
        test_data = dict(username="test", content_id="", content_type=None)

        with self.assertRaises(vm.NoVoteFoundError, msg="Invalid vote"):
            self.vote_manager.get_vote(
                username=test_data["username"],
                content_id=test_data["content_id"],
                content_type=test_data["content_type"],
            )

        with self.assertRaises(vm.InvalidContentType, msg="Invalid content type"):
            self.vote_model.get_vote = lambda vote: test_data
            self.vote_manager.get_vote(
                username=test_data["username"],
                content_id=test_data["content_id"],
                content_type=test_data["content_type"],
            )

        for content_type in vm.ContentType:
            with self.subTest(
                "Ensure unmodified vote with content_type=" + str(content_type)
            ):
                test_data["content_type"] = content_type
                base_vote = test_data.copy()
                base_vote["content_type"] = str(content_type)
                self.vote_model.get_vote = lambda vote, base_vote=base_vote: base_vote
                self.assertEqual(
                    self.vote_manager.get_vote(
                        username=test_data["username"],
                        content_id=test_data["content_id"],
                        content_type=test_data["content_type"],
                    ),
                    test_data,
                )

    def test_add_vote(self):
        self.vote_model.get_vote = lambda vote: None

        test_data = dict(username="test", content_id="")
        test_post = dict(
            op="Test",
            title="Test Post",
            body="Test Body",
            media=None,
            tags=None,
            modified_date=None,
            likes=0,
            dislikes=0,
        )

        def test_vote_addition(msg=None, expect_like_update=True):
            # add vote and update vote essentially act the same way
            self.vote_model.add_vote = set_data_wrapper(self.data)
            self.vote_model.update_vote = set_data_wrapper(self.data)
            self.post_model.get_by_post_id = lambda post_id: test_post

            # Ensure add_like is called for the respective content type
            if expect_like_update:
                self.data["like_update_called"] = False
                if test_data["content_type"] == vm.ContentType.POST:

                    def callback(post_id, data):
                        self.data["like_update_called"] = True
                        return True

                    self.post_model.edit_post = callback

            self.vote_manager.add_vote(
                username=test_data["username"],
                content_id=test_data["content_id"],
                content_type=test_data["content_type"],
                is_like=test_data["is_like"],
            )

            # Translate content type to string
            test_data_copy = test_data.copy()
            test_data_copy["content_type"] = str(test_data["content_type"])

            with self.subTest(msg=msg):
                vote = self.data["args"][0]
                assertTimeInRange(self, vote["creation_date"])

                self.assertEqual(vote, vote | test_data_copy)

                if expect_like_update:
                    self.assertTrue(self.data["like_update_called"])

        for is_like in [True, False]:
            with self.subTest("Posts"):
                test_data["content_type"] = vm.ContentType.POST
                test_data["is_like"] = is_like

                base_vote = test_data.copy()

                with self.assertRaises(vm.InvalidContent, msg="Invalid post"):
                    self.post_model.get_by_post_id = lambda post_id: None
                    self.vote_manager.add_vote(
                        username=test_data["username"],
                        content_id=test_data["content_id"],
                        content_type=test_data["content_type"],
                        is_like=test_data["is_like"],
                    )

                self.vote_model.get_vote = lambda vote: None
                test_vote_addition("Add brand new vote")

                base_vote["content_type"] = str(test_data["content_type"])
                self.vote_model.get_vote = lambda vote, base_vote=base_vote: base_vote
                test_vote_addition(
                    f"Update vote from is_like={is_like} -> is_like={is_like}",
                    expect_like_update=False,
                )

                base_vote["is_like"] = not is_like
                base_vote["content_type"] = str(test_data["content_type"])
                self.vote_model.get_vote = lambda vote, base_vote=base_vote: base_vote
                test_vote_addition(
                    f"Update vote from is_like={not is_like} -> is_like={is_like}"
                )

        with self.assertRaises(vm.InvalidContentType, msg="Invalid content type"):
            test_data["content_type"] = None
            self.vote_manager.add_vote(
                username=test_data["username"],
                content_id=test_data["content_id"],
                content_type=test_data["content_type"],
                is_like=test_data["is_like"],
            )

    def test_remove_vote(self):
        self.vote_model.get_vote = lambda vote: None

        test_data = dict(username="test", content_id="")

        with self.assertRaises(vm.NoVoteFoundError, msg="Invalid vote"):
            self.vote_manager.remove_vote(
                test_data["username"],
                test_data["content_id"],
                None,
            )

        with self.subTest("Posts"):
            test_data["content_type"] = vm.ContentType.POST
            base_vote = test_data.copy()
            base_vote["content_type"] = str(test_data["content_type"])

            with self.assertRaises(
                vm.InvalidContentType, msg="Invalid stored content type"
            ):
                base_vote["content_type"] = "random"
                self.vote_model.get_vote = lambda vote: base_vote
                self.post_model.get_by_post_id = lambda id: None

                self.vote_manager.remove_vote(
                    test_data["username"],
                    test_data["content_id"],
                    test_data["content_type"],
                )

            with self.assertRaises(vm.InvalidContent, msg="Invalid post"):
                base_vote["content_type"] = str(test_data["content_type"])
                self.vote_model.get_vote = lambda vote: base_vote
                self.post_model.get_by_post_id = lambda id: None

                self.vote_manager.remove_vote(
                    test_data["username"],
                    test_data["content_id"],
                    test_data["content_type"],
                )

    def test_clear_votes_by_id(self):
        test_data = {}
        with self.subTest("Ensure callbacks are being utilized"):
            test_data["called"] = False

            def callback(content_id):
                test_data["called"] = True
                return True

            self.vote_model.clear_votes_by_id = callback

            self.vote_manager.clear_votes_by_id("")

            self.assertTrue(test_data["called"])
