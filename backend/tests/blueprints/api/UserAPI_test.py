import unittest

from flask import session

from backend.app import create_app
from backend.blueprints.api.UserAPI import UserAPI
from backend.constants import DATA
from backend.data.managers.UserManager import (
    InvalidPasswordError,
    InvalidUsernameError,
    UserManager,
    UsernameExistsError,
)
from backend.data.models.UserModel import User
from backend.tests.blueprints import (
    TestManagerFactory,
    blueprint_test_raise,
    setup_test_context,
)


class TestUserManager(UserManager):
    def user_exists(self, username: str) -> bool:  # NOSONAR
        pass

    def check_password(
        self, username: str, password: str
    ) -> tuple[bool, User]:  # NOSONAR
        pass

    def create_user(self, username: str, password: str) -> User | None:  # NOSONAR
        pass


class UserEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()

        self.test_manager_factory = TestManagerFactory()

        self.user_manager = TestUserManager()
        self.test_manager_factory.create_user_manager = lambda: self.user_manager

        self.user_api = UserAPI(manager_factory=self.test_manager_factory)

    def test_login(self):
        with self.subTest("Already logged in"):

            def test():
                session[DATA.USER] = dict(username="")

                expected_response = dict(
                    type="AlreadyLoggedIn", error="Already logged in"
                )
                response = self.user_api.login().get_json()
                self.assertEqual(response, expected_response)

            setup_test_context(self.app, test, dict(username="", password=""))

        with self.subTest("Invalid credentials"):

            def test():
                self.user_manager.check_password = lambda username, password: (
                    False,
                    None,
                )

                expected_response = dict(
                    type="ActionFailed", error="Invalid credentials"
                )
                response = self.user_api.login().get_json()
                self.assertEqual(response, expected_response)

            setup_test_context(self.app, test, dict(username="", password=""))

        with self.subTest("Successful login"):

            def test():
                test_data = dict(
                    username="Test",
                    password="Test_Password",
                    registration_date="whatever",
                )
                self.user_manager.check_password = lambda username, password: (
                    True,
                    test_data,
                )

                expected_response = dict(msg="Logged in")
                response = self.user_api.login().get_json()
                self.assertEqual(response, expected_response)

                self.assertEqual(session[DATA.USER], test_data)

            setup_test_context(self.app, test, dict(username="", password=""))

    def test_logout(self):
        def test():
            session[DATA.USER] = dict(username="")

            expected_response = dict(msg="Logged out")
            response = self.user_api.logout().get_json()
            self.assertEqual(response, expected_response)

        setup_test_context(self.app, test)

    def test_register(self):
        request_data = dict(username="", password="")
        with self.subTest("Success"):

            def test():
                test_data = dict(
                    username="Test",
                    password="Test_Password",
                    registration_date="whatever",
                )
                self.user_manager.create_user = lambda username, password: test_data

                expected_response = dict(msg="User created")
                response = self.user_api.register().get_json()
                self.assertEqual(response, expected_response)
                self.assertEqual(session[DATA.USER], test_data)

            setup_test_context(self.app, test, request_data)

        with self.subTest("Fail without raising"):

            def test():
                self.user_manager.create_user = lambda username, password: None

                expected_response = dict(type="ActionFailed", error="Could not create")
                response = self.user_api.register().get_json()
                self.assertEqual(response, expected_response)

            setup_test_context(self.app, test, request_data)

        blueprint_test_raise(
            self,
            self.app,
            self.user_api.register,
            request_data,
            self.user_manager,
            "create_user",
            [UsernameExistsError, InvalidUsernameError, InvalidPasswordError],
        )

    def test_get(self):
        with self.subTest("Not logged in"):

            def test():
                response = self.user_api.get().get_json()
                self.assertEqual(response, {})

            setup_test_context(self.app, test)

        with self.subTest("Logged in"):

            def test():
                test_data = dict(
                    username="Test",
                    password="Test_Password",
                    registration_date="whatever",
                )
                session[DATA.USER] = test_data

                expected_response = test_data.copy()
                del expected_response["password"]

                response = self.user_api.get().get_json()
                self.assertEqual(response, expected_response)

            setup_test_context(self.app, test)
