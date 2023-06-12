import unittest
from backend.tests.data.databases.TestDatabase import TestDatabase
from backend.app import create_app
from backend.JafaConfig import JafaConfig


REGISTER_ENDPOINT = "/api/user/register"
LOGIN_ENDPOINT = "/api/user/login"


def register(client, username, password):
    return client.post(
        REGISTER_ENDPOINT, data={"username": username, "password": password})


def login(client, username, password):
    return client.post(
        LOGIN_ENDPOINT, data={"username": username, "password": password})


class UserEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.config = JafaConfig()
        self.config.database_type = "custom"
        self.config.database_class = TestDatabase

        self.app = create_app()
        self.client = self.app.test_client()

    def test_register(self):
        """We should only check that outputs are formatted
        properly since we have other tests for handling different scenarios

        This thought process should apply to all endpoint testings within this project
        """
        res = self.client.post(REGISTER_ENDPOINT)
        self.assertIn(
            b'{"error":"Missing username and/or password"}', res.data, "Erroneous response")

        res = register(self.client, "red", "Password1")
        self.assertIn(
            b'{"msg":"User created"}', res.data, "Successful response")

    def test_login(self):
        register(self.client, "red", "Password1")
        res = self.client.post(LOGIN_ENDPOINT)
        self.assertIn(
            b'{"error":"Missing username and/or password"}', res.data, "Erroneous response")

        res = login(self.client, "red", "Password1")
        self.assertIn(
            b'{"msg":"Logged in"}', res.data, "Successful response")
