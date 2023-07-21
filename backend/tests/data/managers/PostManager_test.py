import unittest
import sys

import backend.data.managers.PostMananger as pm
from backend.data.managers.SubForumManager import SubForumManager
from backend.tests.data.models.TestModelFactory import TestModelFactory


class PostManagerTestCase(unittest.TestCase):
    def setUp(self):
        TestModelFactory.reset()
        self.post_model = TestModelFactory.create_post_model()
        self.post_manager = pm.PostManager(TestModelFactory)

        # Default subforum to use
        subforum_manager = SubForumManager(TestModelFactory)
        subforum_manager.create_subforum("test", "test", "Test Description")

    def test_create_post(self):
        # Title
        with self.assertRaises(pm.InvalidPostTitle, msg="Empty title"):
            self.post_manager.create_post("test", "test", "", "Test Message")

            # Length
        with self.assertRaises(
            pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MIN - 1"
        ):
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MIN - 1), "Test Message"
            )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MIN), "Test Message"
            ),
            "BOUNDARY: Title = TITLE_MIN",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MIN + 1), "Test Message"
            ),
            "BOUNDARY: Title = TITLE_MIN + 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MAX - 1), "Test Message"
            ),
            "BOUNDARY: Title = TITLE_MAX - 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MAX), "Test Message"
            ),
            "BOUNDARY: Title = TITLE_MAX",
        )

        with self.assertRaises(
            pm.InvalidPostTitle, msg="BOUNDARY: Title = TITLE_MAX + 1"
        ):
            self.post_manager.create_post(
                "test", "test", "T" * (pm.TITLE_MAX + 1), "Test Message"
            )

        # Body

        with self.assertRaises(pm.InvalidPostBody, msg="Empty body"):
            self.post_manager.create_post("test", "test", "Test Title", "")

            # Length
        with self.assertRaises(pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MIN - 1"):
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MIN - 1)
            )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MIN)
            ),
            "BOUNDARY: Body = BODY_MIN",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MIN + 1)
            ),
            "BOUNDARY: Body = BODY_MIN + 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MAX - 1)
            ),
            "BOUNDARY: Body = BODY_MAX - 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MAX)
            ),
            "BOUNDARY: Body = BODY_MAX",
        )

        with self.assertRaises(pm.InvalidPostBody, msg="BOUNDARY: Body = BODY_MAX + 1"):
            self.post_manager.create_post(
                "test", "test", "Test Title", "T" * (pm.BODY_MAX + 1)
            )

        # Tags
        self.post_model.db.clear()
        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "Test Message", None, []
            ),
            "Empty array",
        )

        self.assertIsNone(
            self.post_manager.get_post("0")["tags"], "Empty array tags becomes None"
        )

        # Limit
        self.assertTrue(
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T"] * (pm.TAGS_LIMIT - 1),
            ),
            "BOUNDARY: Tags = TAGS_LIMIT - 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T"] * (pm.TAGS_LIMIT),
            ),
            "BOUNDARY: Tags = TAGS_LIMIT",
        )

        with self.assertRaises(
            pm.TagLimitExceeded, msg="BOUNDARY: Tags = TAGS_LIMIT + 1"
        ):
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T"] * (pm.TAGS_LIMIT + 1),
            )

        # Length
        self.assertTrue(
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T" * (pm.TAG_MAX - 1)],
            ),
            "BOUNDARY: Tags = TAGS_MAX - 1",
        )

        self.assertTrue(
            self.post_manager.create_post(
                "test", "test", "Test Title", "Test Message", None, ["T" * (pm.TAG_MAX)]
            ),
            "BOUNDARY: Tags = TAGS_MAX",
        )

        with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Tags = TAGS_MAX + 1"):
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T" * (pm.TAG_MAX + 1)],
            )

        # Index
        with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at start"):
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                [""] + (["T"] * (pm.TAGS_LIMIT - 1)),
            )

        with self.assertRaises(pm.InvalidPostTag, msg="BOUNDARY: Bad tag at end"):
            self.post_manager.create_post(
                "test",
                "test",
                "Test Title",
                "Test Message",
                None,
                ["T"] * (pm.TAGS_LIMIT - 1) + [""],
            )

        # Check for stripping
        self.post_model.db.clear()
        self.assertTrue(
            self.post_manager.create_post(
                "test",
                "test",
                "  Test Title  ",
                "  Test Message  ",
                None,
                ["  T  "] * pm.TAGS_LIMIT,
            ),
            "VALID with spaces",
        )

        post = self.post_manager.get_post("0")
        self.assertEqual(post["title"], "Test Title", "Stripped title")
        self.assertEqual(post["body"], "Test Message", "Stripped body")
        self.assertEqual(post["tags"], ["T"] * pm.TAGS_LIMIT, "Stripped tags")

    def test_delete_post(self):
        with self.assertRaises(pm.NoPostFoundError, msg="Nonexistant post"):
            self.post_manager.delete_post("test", "test")

        # Permissions
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")
        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            self.post_manager.delete_post("random", "0")

        self.assertTrue(self.post_manager.delete_post("test", "0"), "VALID")

    def test_get_post(self):
        with self.assertRaises(pm.NoPostFoundError, msg="Nonexistant post"):
            self.post_manager.get_post("test")

        self.post_manager.create_post("test", "test", "Test Post", "Test Message")
        self.assertEqual(self.post_manager.get_post("0")["title"], "Test Post")

    def test_lock_post(self):
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")

        self.assertTrue(self.post_manager.lock_post("test", "0"), "VALID")

        with self.assertRaises(pm.PostAlreadyLockedError, msg="Post already locked"):
            self.post_manager.lock_post("test", "0")

        with self.assertRaises(
            pm.PostAlreadyLockedError, msg="Post already locked and not OP"
        ):
            self.post_manager.lock_post("random", "0")

        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            self.post_manager.lock_post("random", "1")

    def test_unlock_post(self):
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")
        self.post_manager.lock_post("test", "0")
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")

        with self.assertRaises(pm.PostNotLockedError, msg="Post not locked"):
            self.post_manager.unlock_post("test", "1")

        with self.assertRaises(pm.PostNotLockedError, msg="Post not locked and not OP"):
            self.post_manager.unlock_post("random", "1")

        with self.assertRaises(pm.RolePermissionError, msg="User not op"):
            self.post_manager.unlock_post("random", "0")

        self.assertTrue(self.post_manager.unlock_post("test", "0"), "VALID")

    def test_add_like(self):
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")

        with self.assertRaises(pm.NoPostFoundError, msg="Invalid post"):
            self.post_manager.add_like("test", False)

        # Dislikes
        self.assertTrue(self.post_manager.add_like("0", False), "Add dislike")
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"], 1, "Dislikes is 1"
        )

        self.assertTrue(self.post_manager.add_like("0", False, False), "Remove dislike")
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"], 0, "Dislikes is 0"
        )

        self.assertTrue(self.post_manager.add_like("0", False, False), "Remove dislike")
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"],
            0,
            "Dislikes didn't become negative",
        )

        ## Simulate a lot of calls
        self.post_model.db["0"]["dislikes"] = 2**1024

        self.assertTrue(self.post_manager.add_like("0", False), "Add dislike")
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"],
            2**1024 + 1,
            "Dislikes is 2 ** 1024 + 1",
        )

        # Likes
        self.assertTrue(self.post_manager.add_like("0", True), "Add like")
        self.assertEqual(self.post_manager.get_post("0")["likes"], 1, "Likes is 1")

        self.assertTrue(self.post_manager.add_like("0", True, False), "Remove like")
        self.assertEqual(self.post_manager.get_post("0")["likes"], 0, "Likes is 0")

        self.assertTrue(self.post_manager.add_like("0", False, False), "Remove like")
        self.assertEqual(
            self.post_manager.get_post("0")["likes"],
            0,
            "Likes didn't become negative",
        )

        ## Simulate a lot of calls
        self.post_model.db["0"]["likes"] = 2**1024

        self.assertTrue(self.post_manager.add_like("0", True), "Add like")
        self.assertEqual(
            self.post_manager.get_post("0")["likes"],
            2**1024 + 1,
            "Likes is 2 ** 1024 + 1",
        )

    def test_post_exists(self):
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")

        self.assertFalse(self.post_manager.post_exists("test"))
        self.assertTrue(self.post_manager.post_exists("0"))

    def test_get_post_list(self):
        # No logic to test
        pass
