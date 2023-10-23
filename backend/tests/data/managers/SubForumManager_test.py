import string
import unittest
from datetime import datetime

import backend.data.managers.SubForumManager as sfm
from backend.data.models.SubForumModel import SubForum, SubForumModel
from backend.tests import assertTimeInRange
from backend.tests.data.managers import TestModelFactory
from backend.tests.data.managers.PostManager_test import TestPostModel
from backend.utils import set_data_wrapper


class TestSubForumModel(SubForumModel):
    def create_subforum(self, data: SubForum) -> bool:  # NOSONAR
        pass

    def delete_subforum(self, title: str) -> bool:  # NOSONAR
        pass

    def edit_subforum(self, title: str, description: str) -> bool:  # NOSONAR
        pass

    def get_subforum_by_title(self, title: str) -> SubForum | None:  # NOSONAR
        pass


class SubForumManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.subforum_model = TestSubForumModel()
        self.post_model = TestPostModel()

        test_model_factory = TestModelFactory()
        test_model_factory.create_subforum_model = lambda: self.subforum_model
        test_model_factory.create_post_model = lambda: self.post_model
        self.subforum_manager = sfm.SubForumManager(test_model_factory)
        self.data = {}

    def test_get_subforum(self):
        self.subforum_model.get_subforum_by_title = lambda title: None

        with self.assertRaises(sfm.NoSubForumFoundError, msg="Invalid subforum"):
            self.subforum_manager.get_subforum("")

        test_data = dict(
            creator="test",
            description="Test description",
            title="Test_Subforum",
            creation_date=datetime.now(),
        )

        self.subforum_model.get_subforum_by_title = lambda title: test_data
        self.assertEqual(
            self.subforum_manager.get_subforum(""),
            test_data,
            "Subforum data is unmodified",
        )

    def test_create_subforum(self):
        self.subforum_model.create_subforum = set_data_wrapper(self.data)
        self.subforum_model.get_subforum_by_title = lambda title: None

        test_data = dict(creator="test", description="Test description", title="")

        def test_subforum_creation(msg=None):
            with self.subTest(msg=msg):
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )
                subforum = self.data["args"][0]
                assertTimeInRange(self, subforum["creation_date"])

                self.assertEqual(subforum, subforum | test_data)

        with self.subTest("Title"):
            with self.assertRaises(sfm.InvalidSubForumTitle, msg="Empty title"):
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

                # Underscores
            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: Start with _"
            ):
                test_data["title"] = "_Test"
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: End with _"
            ):
                test_data["title"] = "Test_"
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

            test_data["title"] = "Test__Subforum"
            test_subforum_creation(msg="VALID: Double underscore")

            test_data["title"] = "Test_Subforum"
            test_subforum_creation(msg="VALID: Single underscore")

            test_data["title"] = "Test_Sub_forum"
            test_subforum_creation(msg="Multiple nonconsecutive underscores")

            # Special characters

            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: Symbol at start"
            ):
                test_data["title"] = "@Test"
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: Symbol at end"
            ):
                test_data["title"] = "Test@"
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

            for char in string.punctuation.replace("_", ""):  # Remove underscore
                with self.assertRaises(
                    sfm.InvalidSubForumTitle, msg=f"Special character: '{char}'"
                ):
                    title = "TestSubforum"
                    # Insert special character in middle
                    middle = len(title) // 2
                    title = title[:middle] + char + title[middle:]
                    test_data["title"] = title

                    self.subforum_manager.create_subforum(
                        test_data["creator"],
                        test_data["title"],
                        test_data["description"],
                    )

                # Length
            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: Title = TITLE_MIN - 1"
            ):
                test_data["title"] = "T" * (sfm.TITLE_MIN - 1)
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

            test_data["title"] = "T" * (sfm.TITLE_MIN)
            test_subforum_creation(msg="BOUNDARY: Title = TITLE_MIN")

            test_data["title"] = "T" * (sfm.TITLE_MIN + 1)
            test_subforum_creation(msg="BOUNDARY: Title = TITLE_MIN + 1")

            test_data["title"] = "T" * (sfm.TITLE_MAX - 1)
            test_subforum_creation(msg="BOUNDARY: Title = TITLE_MAX - 1")

            test_data["title"] = "T" * (sfm.TITLE_MAX)
            test_subforum_creation(msg="BOUNDARY: Title = TITLE_MAX")

            with self.assertRaises(
                sfm.InvalidSubForumTitle, msg="BOUNDARY: Title = TITLE_MAX + 1"
            ):
                test_data["title"] = "T" * (sfm.TITLE_MAX + 1)
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

                # Exists
            self.subforum_model.get_subforum_by_title = lambda title: test_data | {
                "creation_date": datetime.now()
            }
            with self.assertRaises(
                sfm.SubForumTitleExistsError, msg="Duplicate subforum detected"
            ):
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )
            self.subforum_model.get_subforum_by_title = lambda title: None

        with self.subTest("Description"):
            test_data["title"] = "Test"
            # Empty
            with self.assertRaises(
                sfm.InvalidSubForumDescription, msg="Empty description"
            ):
                test_data["description"] = ""
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

                # Length
            test_data["description"] = "T" * (sfm.DESCRIPTION_MAX - 1)
            test_subforum_creation(msg="BOUNDARY: Description = DESCRIPTION_MAX - 1")

            test_data["description"] = "T" * (sfm.DESCRIPTION_MAX)
            test_subforum_creation(msg="BOUNDARY: Description = DESCRIPTION_MAX")

            with self.assertRaises(
                sfm.InvalidSubForumDescription,
                msg="BOUNDARY: Description = DESCRIPTION_MAX + 1",
            ):
                test_data["description"] = "T" * (sfm.DESCRIPTION_MAX + 1)
                self.subforum_manager.create_subforum(
                    test_data["creator"], test_data["title"], test_data["description"]
                )

    def test_delete_subforum(self):
        self.subforum_model.get_subforum_by_title = lambda title: None

        test_data = dict(creator="test", title="Test_SubForum")

        with self.assertRaises(sfm.NoSubForumFoundError, msg="Nonexistant subforum"):
            self.subforum_manager.delete_subforum(
                test_data["creator"], test_data["title"]
            )

        self.subforum_model.get_subforum_by_title = lambda title: test_data
        with self.assertRaises(sfm.RolePermissionError, msg="User not creator"):
            self.subforum_manager.delete_subforum("random", test_data["title"])

        with self.subTest("Ensure callbacks are being utilized"):
            test_data["called"] = False

            def callback(title):
                test_data["called"] = True
                return True

            self.subforum_model.delete_subforum = callback

            self.subforum_manager.delete_subforum(
                test_data["creator"], test_data["title"]
            )

            self.assertTrue(test_data["called"])

    def test_edit_subforum(self):
        self.subforum_model.get_subforum_by_title = lambda title: None

        test_data = dict(
            creator="test", title="Test_SubForum", description="Test description"
        )

        with self.assertRaises(sfm.NoSubForumFoundError, msg="Nonexistant subforum"):
            self.subforum_manager.delete_subforum(
                test_data["creator"], test_data["title"]
            )

        self.subforum_model.get_subforum_by_title = lambda title: test_data
        with self.assertRaises(sfm.RolePermissionError, msg="User not creator"):
            self.subforum_manager.edit_subforum(
                "random", test_data["title"], test_data["description"]
            )

        with self.assertRaises(sfm.InvalidSubForumDescription, msg="Empty description"):
            test_data["description"] = ""
            self.subforum_manager.edit_subforum(
                test_data["creator"], test_data["title"], test_data["description"]
            )

        self.subforum_model.edit_subforum = set_data_wrapper(self.data)
        with self.subTest(
            msg="Ensure callback is called and updated is data is passed unmodified"
        ):
            test_data["description"] = "Test description"

            self.subforum_manager.edit_subforum(
                test_data["creator"], test_data["title"], test_data["description"]
            )

            self.assertEqual(
                (test_data["title"], test_data["description"]), self.data["args"]
            )

    def test_get_subforum_info(self):
        self.subforum_model.get_subforum_by_title = lambda title: None
        self.post_model.get_count = lambda title: 0

        with self.assertRaises(sfm.NoSubForumFoundError, msg="Invalid subforum"):
            self.subforum_manager.get_subforum_info("")

        test_data = dict(
            creator="test",
            title="Test_SubForum",
            description="Test description",
            creation_date=datetime.now(),
        )

        self.subforum_model.get_subforum_by_title = lambda title: test_data
        self.assertEqual(
            self.subforum_manager.get_subforum_info(""),
            test_data | dict(post_count=0, page_count=0, current_page=0),
            "Empty subforum",
        )

        self.assertEqual(
            self.subforum_manager.get_subforum_info("", current_page=5),
            test_data | dict(post_count=0, page_count=0, current_page=5),
            "Empty subforum with non-zero page",
        )

        self.post_model.get_count = lambda title: 100
        self.assertEqual(
            self.subforum_manager.get_subforum_info("", current_page=0, page_limit=10),
            test_data | dict(post_count=100, page_count=10, current_page=0),
            "Subforum with 100 posts, 10 page limit",
        )

        self.assertEqual(
            self.subforum_manager.get_subforum_info("", current_page=0, page_limit=9),
            test_data | dict(post_count=100, page_count=12, current_page=0),
            "Subforum with 100 posts, 9 page limit",
        )

        self.assertEqual(
            self.subforum_manager.get_subforum_info(None, current_page=0, page_limit=9),
            dict(post_count=100, page_count=12, current_page=0),
            "Subforum is None, with 100 posts, 9 page limit",
        )
