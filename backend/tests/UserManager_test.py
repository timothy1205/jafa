import unittest
from bcrypt import hashpw, gensalt
from hashlib import sha256
from base64 import b64encode
import backend.databases.data.UserManager as um
from backend.tests.databases.TestDatabase import TestDatabase


class UserManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.db = TestDatabase()
        self.user_manager = um.UserManager(self.db)

    def test_check_password(self):
        password = b64encode(sha256("Password1".encode("utf-8")).digest())
        hashed = hashpw(password, gensalt())
        user = {"username": "Test", "password": hashed}
        self.db.create(um.USERS_LOCATION, user)

        self.assertEqual(self.user_manager.check_password(
            "Test", "Password1"), (True, user), "Valid password")
        self.assertEqual(self.user_manager.check_password(
            "Test", "Password2"), (False, None), "Wrong character at end of password")
        self.assertEqual(self.user_manager.check_password(
            "Test", "password1"), (False, None), "Wrong character at start of password")

    def test_create_user(self):
        # Username length
        with self.assertRaises(um.InvalidUsernameError, msg="BOUNDARY: Username = USERNAME_MIN - 1"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN - 1), "Password1")

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "Password1"), "BOUNDARY: Username = USERNAME_MIN")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN + 1), "Password1"), "BOUNDARY: Username = USERNAME_MIN + 1")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MAX - 1), "Password1"), "BOUNDARY: Username = USERNAME_MAX - 1")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MAX), "Password1"), "BOUNDARY: Username = USERNAME_MAX")
        self.db.delete(um.USERS_LOCATION, {})

        with self.assertRaises(um.InvalidUsernameError, msg="Username = USERNAME_MAX + 1"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MAX + 1), "Password1")

        # Duplicate username
        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "Password1"), "Valid user")

        with self.assertRaises(um.UsernameExistsError, msg="Duplicate username"):
            self.user_manager.create_user("red", "Password1")
        self.db.delete(um.USERS_LOCATION, {})

        # Password Length
        with self.assertRaises(um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MIN - 1"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "p" * (um.PASSWORD_MIN - 1))

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MIN - 2)), "BOUNDARY: Password = PASSWORD_MIN")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MIN - 1)), "BOUNDARY: Password = PASSWORD_MIN + 1")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MAX - 3)), "BOUNDARY: Password = PASSWORD_MAX - 1")
        self.db.delete(um.USERS_LOCATION, {})

        self.assertTrue(self.user_manager.create_user(
            "r" * (um.USERNAME_MIN), "P1" + "p" * (um.PASSWORD_MAX - 2)), "BOUNDARY: Password = PASSWORD_MAX")
        self.db.delete(um.USERS_LOCATION, {})

        with self.assertRaises(um.InvalidPasswordError, msg="BOUNDARY: Password = PASSWORD_MAX + 1"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "p" * (um.PASSWORD_MAX - 1))

        # Password character types
        with self.assertRaises(um.InvalidPasswordError, msg="Password missing number"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "P" + "p" * (um.PASSWORD_MIN))

        with self.assertRaises(um.InvalidPasswordError, msg="Password missing uppercase"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "1" + "p" * (um.PASSWORD_MIN))

        with self.assertRaises(um.InvalidPasswordError, msg="Password missing lowercase"):
            self.user_manager.create_user(
                "r" * (um.USERNAME_MIN), "1" + "P" * (um.PASSWORD_MIN))