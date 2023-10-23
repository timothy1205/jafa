import sys
import unittest
from datetime import datetime

import backend.data.managers.PostMananger as pm
from backend.data.managers.SubForumManager import NoSubForumFoundError
from backend.data.models.PostModel import BasePost, CreatePost, Post, PostModel
from backend.tests import assertTimeInRange
from backend.tests.data.managers import TestModelFactory
from backend.tests.data.managers.VoteManager_test import TestVoteModel
from backend.utils import set_data_wrapper


class TestPostModel(PostModel):
    def create_post(self, data: CreatePost) -> bool:  # NOSONAR
        pass

    def get_by_post_id(self, post_id: str) -> Post | None:  # NOSONAR
        pass

    def delete_by_post_id(self, post_id: str) -> bool:  # NOSONAR
        pass

    def clear_posts(self, username: str) -> bool:  # NOSONAR
        pass

    def edit_post(self, post_id: str, data: BasePost) -> bool:  # NOSONAR
        pass

    def lock_post(self, post_id: str) -> bool:  # NOSONAR
        pass

    def unlock_post(self, post_id: str) -> bool:  # NOSONAR
        pass

    def get_posts(  # NOSONAR
        self, limit: int, skip: int, subforum: str | None = None
    ) -> list[Post]:
        pass

    def get_count(self, subforum: str | None = None) -> int:  # NOSONAR
        pass


class PostManagerTestCase(unittest.TestCase):
    def setUp(self):
        from backend.tests.data.managers.SubForumManager_test import TestSubForumModel

        self.post_model = TestPostModel()
        self.subforum_model = TestSubForumModel()
        self.vote_model = TestVoteModel()

        test_model_factory = TestModelFactory()
        test_model_factory.create_post_model = lambda: self.post_model
        test_model_factory.create_subforum_model = lambda: self.subforum_model
        test_model_factory.create_vote_model = lambda: self.vote_model
        self.post_manager = pm.PostManager(test_model_factory)
        self.data = {}

    def test_create_post(self):
        self.post_model.create_post = set_data_wrapper(self.data)
        self.post_model.get_by_post_id = lambda post_id: None
        self.subforum_model.get_subforum_by_title = lambda title: None

        test_data = dict(
            subforum="Test_Subforum",
            op="test",
            title="Test Title",
            body="Test Body",
            media=None,
            tags=None,
        )

        def test_post_creation(msg=None, compare_data=None):
            with self.subTest(msg=msg):
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

                post = self.data["args"][0]
                assertTimeInRange(self, post["creation_date"])
                self.assertEqual(post["creation_date"], post["modified_date"])

                compare = compare_data or test_data
                self.assertEqual(post, post | compare)
                self.assertEqual(post["tags"], compare["tags"])
                self.assertEqual(post["media"], compare["media"])

        with self.assertRaises(NoSubForumFoundError):
            self.post_manager.create_post(
                op=test_data["op"],
                subforum=test_data["subforum"],
                title=test_data["title"],
                body=test_data["body"],
                media=test_data["media"],
                tags=test_data["tags"],
            )

        self.subforum_model.get_subforum_by_title = lambda title: {}
        with self.subTest("Title"):
            with self.assertRaises(pm.InvalidPostTitle, msg="Empty title"):
                test_data["title"] = ""
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Length
            with self.assertRaises(
                pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MIN - 1"
            ):
                test_data["title"] = "T" * (pm.TITLE_MIN - 1)
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["title"] = "T" * (pm.TITLE_MIN)
            test_post_creation("BOUNDARY: Title = TITLE_MIN")

            test_data["title"] = "T" * (pm.TITLE_MIN + 1)
            test_post_creation("BOUNDARY: Title = TITLE_MIN + 1")

            test_data["title"] = "T" * (pm.TITLE_MAX - 1)
            test_post_creation("BOUNDARY: Title = TITLE_MAX - 1")

            test_data["title"] = "T" * (pm.TITLE_MAX)
            test_post_creation("BOUNDARY: Title = TITLE_MAX")

            with self.assertRaises(
                pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MAX + 1"
            ):
                test_data["title"] = "T" * (pm.TITLE_MAX + 1)
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["title"] = "                           Test Post          "
            compare_data = test_data.copy()
            compare_data["title"] = "Test Post"
            test_post_creation("Strip spaces", compare_data=compare_data)

        with self.subTest("Body"):
            test_data["title"] = "Test Post"

            with self.assertRaises(pm.InvalidPostBody, msg="Empty body"):
                test_data["body"] = ""
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            with self.assertRaises(
                pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MIN - 1"
            ):
                test_data["body"] = "T" * (pm.BODY_MIN - 1)
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["body"] = "T" * (pm.BODY_MIN)
            test_post_creation("BOUNDARY: Body = BODY_MIN")

            test_data["body"] = "T" * (pm.BODY_MIN + 1)
            test_post_creation("BOUNDARY: Body = BODY_MIN + 1")

            test_data["body"] = "T" * (pm.BODY_MAX - 1)
            test_post_creation("BOUNDARY: Body = BODY_MAX - 1")

            test_data["body"] = "T" * (pm.BODY_MAX)
            test_post_creation("BOUNDARY: Body = BODY_MAX")

            with self.assertRaises(
                pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MAX + 1"
            ):
                test_data["body"] = "T" * (pm.BODY_MAX + 1)
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["body"] = "                           Test Body          "
            compare_data = test_data.copy()
            compare_data["body"] = "Test Body"
            test_post_creation("Strip spaces", compare_data=compare_data)

        with self.subTest("Tags"):
            test_data["body"] = "Test Body"
            test_data["tags"] = []
            compare_data = test_data.copy()

            compare_data["tags"] = None
            test_post_creation(
                compare_data=compare_data, msg="Empty tags array becomes None"
            )

            # Limit
            test_data["tags"] = ["T"] * (pm.TAGS_LIMIT - 1)
            test_post_creation("BOUNDARY: Tags = TAGS_LIMIT - 1")

            test_data["tags"] = ["T"] * (pm.TAGS_LIMIT)
            test_post_creation("BOUNDARY: Tags = TAGS_LIMIT")

            with self.assertRaises(
                pm.TagLimitExceeded, msg="BOUNDARY: Tags = TAGS_LIMIT + 1"
            ):
                test_data["tags"] = ["T"] * (pm.TAGS_LIMIT + 1)
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Length
            test_data["tags"] = ["T" * (pm.TAG_MAX - 1)]
            test_post_creation("BOUNDARY: Tags = TAG_MAX - 1")

            test_data["tags"] = ["T" * (pm.TAG_MAX)]
            test_post_creation("BOUNDARY: Tags = TAG_MAX")

            with self.assertRaises(
                pm.InvalidPostTag, msg="BOUNDARY: Tags = TAG_MAX + 1"
            ):
                test_data["tags"] = ["T" * (pm.TAG_MAX + 1)]
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Index
            with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at start"):
                test_data["tags"] = ["", "T", "T"]
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at start"):
                test_data["tags"] = ["T", "T", ""]
                self.post_manager.create_post(
                    op=test_data["op"],
                    subforum=test_data["subforum"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["tags"] = ["   T   ", "           T   ", "   T      "]
            compare_data = test_data.copy()
            compare_data["tags"] = ["T", "T", "T"]
            test_post_creation("Strip spaces", compare_data=compare_data)

    def test_edit_post(self):
        self.post_model.edit_post = set_data_wrapper(self.data)
        self.post_model.get_by_post_id = lambda post_id: None

        test_data = dict(
            post_id="",
            username="test",
            title="Test Title",
            body="Test Body",
            media=None,
            tags=None,
            likes=0,
            dislikes=0,
        )

        post_data = test_data.copy()
        post_data["op"] = test_data["username"]
        del post_data["username"]
        del post_data["post_id"]

        def test_post_creation(msg=None, compare_data={}):
            with self.subTest(msg=msg):
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

                # Format how edit_post returns data
                post_data = test_data.copy()
                post_data["op"] = test_data["username"]
                del post_data["username"]
                del post_data["post_id"]

                post = self.data["args"][1]
                assertTimeInRange(self, post["modified_date"])

                compare = post_data | compare_data
                self.assertEqual(post, post | compare)
                self.assertEqual(post["tags"], compare["tags"])
                self.assertEqual(post["media"], compare["media"])

        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Nonexistant post"):
            self.post_manager.edit_post(
                username=test_data["username"],
                post_id=test_data["post_id"],
                title=test_data["title"],
                body=test_data["body"],
                media=test_data["media"],
                tags=test_data["tags"],
            )

        self.post_model.get_by_post_id = lambda post_id: post_data
        with self.subTest("Title"):
            with self.assertRaises(pm.InvalidPostTitle, msg="Empty title"):
                test_data["title"] = ""
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Length
            with self.assertRaises(
                pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MIN - 1"
            ):
                test_data["title"] = "T" * (pm.TITLE_MIN - 1)
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["title"] = "T" * (pm.TITLE_MIN)
            test_post_creation("BOUNDARY: Title = TITLE_MIN")

            test_data["title"] = "T" * (pm.TITLE_MIN + 1)
            test_post_creation("BOUNDARY: Title = TITLE_MIN + 1")

            test_data["title"] = "T" * (pm.TITLE_MAX - 1)
            test_post_creation("BOUNDARY: Title = TITLE_MAX - 1")

            test_data["title"] = "T" * (pm.TITLE_MAX)
            test_post_creation("BOUNDARY: Title = TITLE_MAX")

            with self.assertRaises(
                pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MAX + 1"
            ):
                test_data["title"] = "T" * (pm.TITLE_MAX + 1)
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["title"] = "                           Test Post          "
            compare_data = dict(title="Test Post")
            test_post_creation("Strip spaces", compare_data=compare_data)

        with self.subTest("Body"):
            test_data["title"] = "Test Post"

            with self.assertRaises(pm.InvalidPostBody, msg="Empty body"):
                test_data["body"] = ""
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            with self.assertRaises(
                pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MIN - 1"
            ):
                test_data["body"] = "T" * (pm.BODY_MIN - 1)
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["body"] = "T" * (pm.BODY_MIN)
            test_post_creation("BOUNDARY: Body = BODY_MIN")

            test_data["body"] = "T" * (pm.BODY_MIN + 1)
            test_post_creation("BOUNDARY: Body = BODY_MIN + 1")

            test_data["body"] = "T" * (pm.BODY_MAX - 1)
            test_post_creation("BOUNDARY: Body = BODY_MAX - 1")

            test_data["body"] = "T" * (pm.BODY_MAX)
            test_post_creation("BOUNDARY: Body = BODY_MAX")

            with self.assertRaises(
                pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MAX + 1"
            ):
                test_data["body"] = "T" * (pm.BODY_MAX + 1)
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["body"] = "                           Test Body          "
            compare_data = dict(body="Test Body")
            test_post_creation("Strip spaces", compare_data=compare_data)

        with self.subTest("Tags"):
            test_data["body"] = "Test Body"
            test_data["tags"] = []
            compare_data = dict(tags=None)
            test_post_creation(
                compare_data=compare_data, msg="Empty tags array becomes None"
            )

            # Limit
            test_data["tags"] = ["T"] * (pm.TAGS_LIMIT - 1)
            test_post_creation("BOUNDARY: Tags = TAGS_LIMIT - 1")

            test_data["tags"] = ["T"] * (pm.TAGS_LIMIT)
            test_post_creation("BOUNDARY: Tags = TAGS_LIMIT")

            with self.assertRaises(
                pm.TagLimitExceeded, msg="BOUNDARY: Tags = TAGS_LIMIT + 1"
            ):
                test_data["tags"] = ["T"] * (pm.TAGS_LIMIT + 1)
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Length
            test_data["tags"] = ["T" * (pm.TAG_MAX - 1)]
            test_post_creation("BOUNDARY: Tags = TAG_MAX - 1")

            test_data["tags"] = ["T" * (pm.TAG_MAX)]
            test_post_creation("BOUNDARY: Tags = TAG_MAX")

            with self.assertRaises(
                pm.InvalidPostTag, msg="BOUNDARY: Tags = TAG_MAX + 1"
            ):
                test_data["tags"] = ["T" * (pm.TAG_MAX + 1)]
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            # Index
            with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at start"):
                test_data["tags"] = ["", "T", "T"]
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at start"):
                test_data["tags"] = ["T", "T", ""]
                self.post_manager.edit_post(
                    username=test_data["username"],
                    post_id=test_data["post_id"],
                    title=test_data["title"],
                    body=test_data["body"],
                    media=test_data["media"],
                    tags=test_data["tags"],
                )

            test_data["tags"] = ["   T   ", "           T   ", "   T      "]
            compare_data = dict(tags=["T", "T", "T"])
            test_post_creation("Strip spaces", compare_data=compare_data)

    def test_delete_post(self):
        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Nonexistant post"):
            self.post_manager.delete_post("", "")

        test_data = dict(op="test")
        self.post_model.get_by_post_id = lambda post_id: test_data
        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            self.post_manager.delete_post("random", "")

        with self.subTest("Ensure callbacks are being utilized"):
            # Don't need to test vote_manager here
            self.vote_model.clear_votes_by_id = lambda contend_id: True

            test_data["called"] = False

            def callback(post_id):
                test_data["called"] = True
                return True

            self.post_model.delete_by_post_id = callback

            self.post_manager.delete_post(test_data["op"], "")

            self.assertTrue(test_data["called"])

    def test_get_post(self):
        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Nonexistant post"):
            self.post_manager.get_post("")

        test_data = dict(
            op="Test",
            title="Test Post",
            body="Test Body",
            media=None,
            tags=None,
            modified_date=datetime.now(),
            likes=0,
            dislikes=0,
        )

        self.post_model.get_by_post_id = lambda post_id: test_data
        self.assertEqual(
            self.post_manager.get_post(""), test_data, "Post data is unmodified"
        )

    def test_lock_post(self):
        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Invalid post"):
            self.post_manager.unlock_post("", "")

        test_data = dict(op="test", locked=True)
        self.post_model.get_by_post_id = lambda post_id: test_data

        with self.assertRaises(pm.PostAlreadyLockedError, msg="Post already locked"):
            self.post_manager.lock_post(test_data["op"], "")

        with self.assertRaises(
            pm.PostAlreadyLockedError, msg="Post already locked and not OP"
        ):
            self.post_manager.lock_post("random", "")

        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            test_data["locked"] = False
            self.post_manager.lock_post("random", "")

        with self.subTest("Ensure callbacks are being utilized"):
            test_data["called"] = False

            def callback(post_id):
                test_data["called"] = True
                return True

            self.post_model.lock_post = callback

            self.post_manager.lock_post(test_data["op"], "")

            self.assertTrue(test_data["called"])

    def test_unlock_post(self):
        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Invalid post"):
            self.post_manager.unlock_post("", "")

        test_data = dict(op="test", locked=False)
        self.post_model.get_by_post_id = lambda post_id: test_data

        with self.assertRaises(pm.PostNotLockedError, msg="Post not locked"):
            self.post_manager.unlock_post(test_data["op"], "")

        with self.assertRaises(pm.PostNotLockedError, msg="Post not locked and not OP"):
            self.post_manager.unlock_post("random", "")

        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            test_data["locked"] = True
            self.post_manager.unlock_post("random", "")

        with self.subTest("Ensure callbacks are being utilized"):
            test_data["called"] = False

            def callback(post_id):
                test_data["called"] = True
                return True

            self.post_model.unlock_post = callback

            self.post_manager.unlock_post(test_data["op"], "")

            self.assertTrue(test_data["called"])

    def test_add_like(self):
        test_data = dict(
            op="Test",
            title="Test Post",
            body="Test Body",
            media=None,
            tags=None,
            modified_date=datetime.now(),
            likes=0,
            dislikes=0,
        )

        self.post_model.get_by_post_id = lambda post_id: None
        with self.assertRaises(pm.NoPostFoundError, msg="Invalid post"):
            self.post_manager.add_like("test", False)

        self.post_model.get_by_post_id = lambda post_id: test_data
        self.post_model.edit_post = set_data_wrapper(self.data)

        with self.subTest("Run tests as likes and dislikes"):
            for is_like, key in [(True, "likes"), (False, "dislikes")]:
                with self.subTest("Increment"):
                    self.post_manager.add_like(
                        post_id="", is_like=is_like, positive=True
                    )
                    self.assertEqual(self.data["args"][1][key], 1)

                with self.subTest("Decrement"):
                    self.post_manager.add_like(
                        post_id="", is_like=is_like, positive=False
                    )
                    self.assertEqual(self.data["args"][1][key], 0)

                with self.subTest("No negatives"):
                    self.post_manager.add_like(
                        post_id="", is_like=is_like, positive=False
                    )
                    self.assertEqual(self.data["args"][1][key], 0)

                with self.subTest("Simulate a lot of calls"):
                    test_data[key] = 2**1024
                    self.post_manager.add_like(
                        post_id="", is_like=is_like, positive=True
                    )
                    self.assertEqual(self.data["args"][1][key], 2**1024 + 1)

    def test_post_exists(self):
        self.post_model.get_by_post_id = lambda post_id: None
        self.assertFalse(self.post_manager.post_exists(""))

        self.post_model.get_by_post_id = lambda post_id: {}
        self.assertTrue(self.post_manager.post_exists(""))

    def test_get_post_list(self):
        with self.subTest("Test for OverflowError"):

            def raise_overflow(limit, skip, subforum):
                raise OverflowError()

            self.post_model.get_posts = raise_overflow

            with self.assertRaises(pm.InvalidPageError):
                self.post_manager.get_post_list("")

        self.post_model.get_posts = set_data_wrapper(self.data)
        test_data = dict(title="Test_Subforum")
        with self.subTest("Pagelimit of 10, page 0"):
            self.post_manager.get_post_list(
                subforum=test_data["title"], page=0, page_limit=10
            )

            self.assertEqual(
                self.data["args"],
                (10, 0, test_data["title"]),
            )

        with self.subTest("Pagelimit of 10, page 50"):
            self.post_manager.get_post_list(
                subforum=test_data["title"], page=50, page_limit=10
            )

            self.assertEqual(
                self.data["args"],
                (10, 500, test_data["title"]),
            )
