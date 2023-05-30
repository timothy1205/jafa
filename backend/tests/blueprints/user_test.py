import unittest
from backend.tests.databases.TestDatabase import TestDatabase
from backend.app import create_app
from backend.JafaConfig import JafaConfig


class userEndpointTestCase(unittest.TestCase):
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
        res = self.client.post("/api/user/register")
        self.assertIn(
            b'{"error":"Missing username and/or password"}', res.data, "Erroneous response")

        res = self.client.post(
            "/api/user/register", data={"username": "red", "password": "Password1"})
        self.assertIn(
            b'{"msg":"User created"}', res.data, "Successful response")

    def test_login(self):
        self.client.post(
            "/api/user/register", data={"username": "red", "password": "Password1"})
        res = self.client.post("/api/user/login")
        self.assertIn(
            b'{"error":"Missing username and/or password"}', res.data, "Erroneous response")

        res = self.client.post(
            "/api/user/login", data={"username": "red", "password": "Password1"})
        self.assertIn(
            b'{"msg":"Logged in"}', res.data, "Successful response")
