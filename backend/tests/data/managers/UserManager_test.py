import string
import unittest
from base64 import b64encode
from hashlib import sha256

from bcrypt import gensalt, hashpw

import backend.data.managers.UserManager as um
from backend.tests.data.models.TestModelFactory import TestModelFactory


class UserManagerTestCase(unittest.TestCase):
    def setUp(self):
        TestModelFactory.reset()
        self.user_model = TestModelFactory.create_user_model()
        self.user_manager = um.UserManager(TestModelFactory)

    def test_check_password(self):
        password = b64encode(sha256("Password1".encode("utf-8")).digest())
        hashed = hashpw(password, gensalt())
        self.user_model.create_user(
            dict(username="Test", password=hashed, registration_date=0)
        )

        result = self.user_manager.check_password("Test", "Password1")
        self.assertTrue(result[0], "Returns True on success")
        self.assertEqual(result[1], result[1] | dict(username="Test", password=hashed))

        self.assertEqual(
            self.user_manager.check_password("Test", "Password2"),
            (False, None),
            "Wrong character at end of password",
        )
        self.assertEqual(
            self.user_manager.check_password("Test", "password1"),
            (False, None),
            "Wrong character at start of password",
        )

    def test_create_user(self):
        # Username length
        with self.assertRaises(
            um.InvalidUsernameError, msg="BOUNDARY: Username = USERNAME_MIN - 1"
        ):
            self.user_manager.create_user("r" * (um.USERNAME_MIN - 1), "Password1")

        self.assertTrue(
            self.user_manager.create_user("r" * (um.USERNAME_MIN), "Password1"),
            "BOUNDARY: Username = USERNAME_MIN",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN))

        self.assertTrue(
            self.user_manager.create_user("r" * (um.USERNAME_MIN + 1), "Password1"),
            "BOUNDARY: Username = USERNAME_MIN + 1",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN + 1))

        self.assertTrue(
            self.user_manager.create_user("r" * (um.USERNAME_MAX - 1), "Password1"),
            "BOUNDARY: Username = USERNAME_MAX - 1",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MAX - 1))

        self.assertTrue(
            self.user_manager.create_user("r" * (um.USERNAME_MAX), "Password1"),
            "BOUNDARY: Username = USERNAME_MAX",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MAX))

        with self.assertRaises(
            um.InvalidUsernameError, msg="BOUNDARY: Username = USERNAME_MAX + 1"
        ):
            self.user_manager.create_user("r" * (um.USERNAME_MAX + 1), "Password1")

        # Username consists only of alphanum characters
        with self.assertRaises(
            um.InvalidUsernameError, msg="BOUNDARY: Symbol at start"
        ):
            self.user_manager.create_user(
                "@" + "r" * (um.USERNAME_MIN - 1), "Password1"
            )

        with self.assertRaises(um.InvalidUsernameError, msg="BOUNDARY: Symbol at end"):
            self.user_manager.create_user(
                "@" + "r" * (um.USERNAME_MIN - 1), "Password1"
            )

        for char in string.punctuation:
            with self.assertRaises(
                um.InvalidUsernameError, msg=f"Special character: '{char}'"
            ):
                username = "r" * (um.USERNAME_MIN * 2)
                # Insert special character in middle
                middle = len(username) // 2
                username = username[:middle] + char + username[middle:]
                self.user_manager.create_user(username, "Password1")

        # Duplicate username
        self.assertTrue(self.user_manager.create_user("red", "Password1"), "Valid user")

        with self.assertRaises(um.UsernameExistsError, msg="Duplicate username"):
            self.user_manager.create_user("red", "Password1")
        self.user_model.delete_user("red")

        # Password Length
        with self.assertRaises(
            um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MIN - 1"
        ):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "p" * (um.PASSWORD_MIN - 1)
            )

        self.assertTrue(
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MIN - 2)
            ),
            "BOUNDARY: Password = PASSWORD_MIN",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN))

        self.assertTrue(
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MIN - 1)
            ),
            "BOUNDARY: Password = PASSWORD_MIN + 1",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN))

        self.assertTrue(
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MAX - 3)
            ),
            "BOUNDARY: Password = PASSWORD_MAX - 1",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN))

        self.assertTrue(
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MAX - 2)
            ),
            "BOUNDARY: Password = PASSWORD_MAX",
        )
        self.user_model.delete_user("r" * (um.USERNAME_MIN))

        with self.assertRaises(
            um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MAX + 1"
        ):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "p" * (um.PASSWORD_MAX - 1)
            )

        # Password character types
        with self.assertRaises(um.InvalidPasswordError, msg="Password missing number"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P" + "p" * (um.PASSWORD_MIN)
            )

        with self.assertRaises(
            um.InvalidPasswordError, msg="Password missing uppercase"
        ):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "1" + "p" * (um.PASSWORD_MIN)
            )

        with self.assertRaises(
            um.InvalidPasswordError, msg="Password missing lowercase"
        ):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "1" + "P" * (um.PASSWORD_MIN)
            )
