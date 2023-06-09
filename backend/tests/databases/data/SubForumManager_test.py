import unittest
import string
import backend.databases.data.SubForumManager as sfm
from backend.tests.databases.TestDatabase import TestDatabase


class SubForumManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.db = TestDatabase()
        self.subforum_manager = sfm.SubForumManager(self.db)

    def test_create_subforum(self):
        test_description = "Test subforum"

        # Title

        with self.assertRaises(sfm.InvalidTitleError, msg="Empty title"):
            self.subforum_manager.create_subforum("test", "", test_description)

            # Underscores
        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: Start with _"):
            self.subforum_manager.create_subforum(
                "test", "_Test", test_description)

        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: End with _"):
            self.subforum_manager.create_subforum(
                "test", "Test_", test_description)

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test__Subforum", test_description), "VALID: Double underscore")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test_Subforum", test_description), "VALID: Single underscore")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test_Sub_forum", test_description), "VALID: Multiple nonconsecutive underscores")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        # Special characters
        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: Symbol at start"):
            self.subforum_manager.create_subforum(
                "test", "@Test", test_description)

        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: Symbol at end"):
            self.subforum_manager.create_subforum(
                "test", "Test@", test_description)

        for char in string.punctuation.replace("_", ""):  # Remove underscore
            with self.assertRaises(sfm.InvalidTitleError, msg=f"Special character: '{char}'"):
                title = "TestSubforum"
                # Insert special character in middle
                middle = len(title) // 2
                title = title[:middle] + char + title[middle:]
                self.subforum_manager.create_subforum(
                    "test", title, test_description)

            # Length
        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: Title = TITLE_MIN - 1"):
            self.subforum_manager.create_subforum(
                "test", "T" * (sfm.TITLE_MIN - 1), test_description)

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "T" * (sfm.TITLE_MIN), test_description), "BOUNDARY: Title = TITLE_MIN")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "T" * (sfm.TITLE_MIN + 1), test_description), "BOUNDARY: Title = TITLE_MIN + 1")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "T" * (sfm.TITLE_MAX - 1), test_description), "BOUNDARY: Title = TITLE_MAX - 1")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "T" * (sfm.TITLE_MAX), test_description), "BOUNDARY: Title = TITLE_MAX")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        with self.assertRaises(sfm.InvalidTitleError, msg="BOUNDARY: Title = TITLE_MAX + 1"):
            self.subforum_manager.create_subforum(
                "test", "T" * (sfm.TITLE_MAX + 1), test_description)

            # Exists
        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test_SubForum", test_description), "VALID")
        with self.assertRaises(sfm.TitleExistsError, msg="BOUNDARY: Title = TITLE_MAX + 1"):
            self.subforum_manager.create_subforum(
                "test", "Test_SubForum", test_description)
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        # Description
        # Empty
        with self.assertRaises(sfm.InvalidDescriptionError, msg="Empty description"):
            self.subforum_manager.create_subforum("test", "Test", "")

            # Length
        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test_SubForum", "T" * (sfm.DESCRIPTION_MAX - 1)), "BOUNDARY: Description = DESCRIPTION_MAX - 1")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        self.assertTrue(self.subforum_manager.create_subforum(
            "test", "Test_SubForum", "T" * (sfm.DESCRIPTION_MAX)), "BOUNDARY: Description = DESCRIPTION_MAX")
        self.db.delete(sfm.SUBFORUM_LOCATION, {})

        with self.assertRaises(sfm.InvalidDescriptionError, msg="BOUNDARY: Description = DESCRIPTION_MAX + 1"):
            self.subforum_manager.create_subforum(
                "test", "Test_SubForum", "T" * (sfm.DESCRIPTION_MAX + 1))

    def test_delete_subforum(self):
        with self.assertRaises(sfm.NoTitleFoundError, msg="Nonexistant subforum"):
            self.subforum_manager.delete_subforum("test", "Test_SubForum")

        # Permissions
        self.subforum_manager.create_subforum(
            "test", "Test_SubForum", "Test subforum")
        with self.assertRaises(sfm.RolePermissionError, msg="User not creator"):
            self.subforum_manager.delete_subforum("random", "Test_SubForum")

        self.assertTrue(self.subforum_manager.delete_subforum(
            "test", "Test_SubForum"), "Valid")
