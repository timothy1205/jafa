import string
import unittest
from base64 import b64encode
from hashlib import sha256

from bcrypt import gensalt, hashpw

import backend.data.managers.UserManager as um
from backend.data.models.UserModel import User, UserModel
from backend.tests import assertTimeInRange
from backend.tests.data.managers import TestModelFactory
from backend.utils import set_data_wrapper


class TestUserModel(UserModel):
    def create_user(self, data: User) -> bool:
        pass

    def get_by_username(self, username: str) -> User | None:
        pass

    def delete_user(self, username: str) -> bool:
        pass


class UserManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.user_model = TestUserModel()

        test_model_factory = TestModelFactory()
        test_model_factory.create_user_model = lambda: self.user_model
        self.user_manager = um.UserManager(test_model_factory)
        self.data = {}

    def test_user_exists(self):
        with self.subTest("No user"):
            self.user_model.get_by_username = lambda username: None
            self.assertFalse(self.user_manager.user_exists(""))

        with self.subTest("Valid user"):
            self.user_model.get_by_username = lambda username: {}
            self.assertTrue(self.user_manager.user_exists(""))

    def test_check_password(self):
        self.user_model.get_by_username = lambda username: None
        self.assertEqual(
            self.user_manager.check_password("", ""),
            (False, None),
            "Invalid user",
        )

        password_clear = "TestPassword"
        password_encoded = b64encode(sha256(password_clear.encode("utf-8")).digest())
        password_hashed = hashpw(password_encoded, gensalt())
        test_data = dict(password=password_hashed)
        self.user_model.get_by_username = lambda username: test_data

        with self.subTest("Hashes match"):
            result, user = self.user_manager.check_password("", password_clear)
            self.assertTrue(result)
            self.assertEqual(user, user | test_data)

        self.assertEqual(
            self.user_manager.check_password("", password_clear + "T"),
            (False, None),
            "Wrong character at end of password",
        )

        self.assertEqual(
            self.user_manager.check_password("", "T" + password_clear),
            (False, None),
            "Wrong character at start of password",
        )

        self.assertEqual(
            self.user_manager.check_password(
                "", password_clear[:4] + "T" + password_clear[4:]
            ),
            (False, None),
            "Wrong character in middle of password",
        )

    def test_create_user(self):
        self.user_model.create_user = set_data_wrapper(self.data)
        self.user_model.get_by_username = lambda username: None

        test_data = dict(username="Test", password="Password1")

        def test_user_creation(msg=None):
            with self.subTest(msg=msg):
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )
                user = self.data["args"][0]
                assertTimeInRange(self, user["registration_date"])

                self.assertEqual(user["username"], test_data["username"])
                # Password should always be hashed
                self.assertNotEqual(user["password"], test_data["password"])

        with self.subTest("Username"):
            # Username length
            with self.assertRaises(
                um.InvalidUsernameError, msg="BOUNDARY: Username = USERNAME_MIN - 1"
            ):
                test_data["username"] = "r" * (um.USERNAME_MIN - 1)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            test_data["username"] = "r" * (um.USERNAME_MIN)
            test_user_creation("BOUNDARY: Username = USERNAME_MIN")

            test_data["username"] = "r" * (um.USERNAME_MIN + 1)
            test_user_creation("BOUNDARY: Username = USERNAME_MIN + 1")

            test_data["username"] = "r" * (um.USERNAME_MAX - 1)
            test_user_creation("BOUNDARY: Username = USERNAME_MAX - 1")

            test_data["username"] = "r" * (um.USERNAME_MAX)
            test_user_creation("BOUNDARY: Username = USERNAME_MAX")

            with self.assertRaises(
                um.InvalidUsernameError, msg="BOUNDARY: Username = USERNAME_MAX + 1"
            ):
                test_data["username"] = "r" * (um.USERNAME_MAX + 1)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            # Username consists only of alphanum characters
            with self.assertRaises(
                um.InvalidUsernameError, msg="BOUNDARY: Symbol at start"
            ):
                test_data["username"] = "@" + "r" * (um.USERNAME_MIN - 1)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            with self.assertRaises(
                um.InvalidUsernameError, msg="BOUNDARY: Symbol at end"
            ):
                test_data["username"] = "r" * (um.USERNAME_MIN - 1) + "@"
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            for char in string.punctuation:
                with self.assertRaises(
                    um.InvalidUsernameError, msg=f"Special character: '{char}'"
                ):
                    username = "r" * (um.USERNAME_MIN * 2)
                    # Insert special character in middle
                    middle = len(username) // 2
                    test_data["username"] = username[:middle] + char + username[middle:]

                    self.user_manager.create_user(
                        test_data["username"], test_data["password"]
                    )

        with self.subTest("Password"):
            test_data["username"] = "test"

            # Password Length
            with self.assertRaises(
                um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MIN - 1"
            ):
                test_data["password"] = "P1" + "p" * (um.PASSWORD_MIN - 3)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            test_data["password"] = "P1" + "p" * (um.PASSWORD_MIN - 2)
            test_user_creation("BOUNDARY: Password = PASSWORD_MIN")

            test_data["password"] = "P1" + "p" * (um.PASSWORD_MIN - 1)
            test_user_creation("BOUNDARY: Password = PASSWORD_MIN + 1")

            test_data["password"] = "P1" + "p" * (um.PASSWORD_MAX - 3)
            test_user_creation("BOUNDARY: Password = PASSWORD_MAX - 1")

            test_data["password"] = "P1" + "p" * (um.PASSWORD_MAX - 2)
            test_user_creation("BOUNDARY: Password = PASSWORD_MAX")

            with self.assertRaises(
                um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MAX + 1"
            ):
                test_data["password"] = "P1" + "p" * (um.PASSWORD_MAX - 1)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            # Password character types
            with self.assertRaises(
                um.InvalidPasswordError, msg="Password missing number"
            ):
                test_data["password"] = "P" + "p" * (um.PASSWORD_MIN)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            with self.assertRaises(
                um.InvalidPasswordError, msg="Password missing uppsercase"
            ):
                test_data["password"] = "1" + "p" * (um.PASSWORD_MIN)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

            with self.assertRaises(
                um.InvalidPasswordError, msg="Password missing lowercase"
            ):
                test_data["password"] = "1" + "P" * (um.PASSWORD_MIN)
                self.user_manager.create_user(
                    test_data["username"], test_data["password"]
                )

        with self.assertRaises(um.UsernameExistsError, msg="Duplicate user"):
            self.user_model.get_by_username = lambda username: {}

            test_data["username"] = "test"
            self.user_manager.create_user(test_data["username"], test_data["password"])
