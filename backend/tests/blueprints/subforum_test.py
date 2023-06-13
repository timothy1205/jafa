from flask import g
import unittest
from backend.app import create_app
from backend.JafaConfig import JafaConfig
from backend.tests.blueprints.user_test import login, register
from backend.tests.data.models.TestModelFactory import TestModelFactory

CREATE_ENDPOINT = "/api/subforum/create"
DELETE_ENDPOINT = "/api/subforum/delete"
EDIT_ENDPOINT = "/api/subforum/edit"


def create(client, title, description):
    return client.post(
        CREATE_ENDPOINT, data={"title": title, "description": description})


class SubForumEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.config = JafaConfig()
        self.config.database_type = "testing"

        self.app = create_app()

        with self.app.app_context():
            TestModelFactory.reset()

        @self.app.before_request
        def before_request():
            g.injected_model_factory = TestModelFactory

        self.client = self.app.test_client()

    def test_create(self):
        """We should only check that outputs are formatted
        properly since we have other tests for handling different scenarios

        This thought process should apply to all endpoint testings within this project
        """
        register(self.client, "red", "Password1")
        login(self.client, "red", "Password1")

        res = self.client.post(CREATE_ENDPOINT)
        self.assertIn(
            f'{{"error":"Missing: {sorted(["title", "description"])}"}}'.encode(
                'utf-8'),
            res.data, "Erroneous response")

        res = create(self.client, "TestSubforum", "Test subforum")
        self.assertIn(
            b'{"msg":"Subforum created"}',
            res.data, "Successful response")

    def test_delete(self):
        register(self.client, "red", "Password1")
        login(self.client, "red", "Password1")

        create(self.client, "TestSubforum", "Test subforum")

        res = self.client.delete(DELETE_ENDPOINT)
        self.assertIn(
            f'{{"error":"Missing: {["title"]}"}}'.encode(
                'utf-8'),
            res.data, "Erroneous response")

        res = self.client.delete(DELETE_ENDPOINT, data={
                                 "title": "TestSubforum"})
        self.assertIn(
            b'{"msg":"Subforum deleted"}',
            res.data, "Successful response")

    def test_edit(self):
        register(self.client, "red", "Password1")
        login(self.client, "red", "Password1")

        create(self.client, "TestSubforum", "Test subforum")

        res = self.client.post(EDIT_ENDPOINT)
        self.assertIn(
            f'{{"error":"Missing: {sorted(["title", "description"])}"}}'.encode(
                'utf-8'),
            res.data, "Erroneous response")

        res = self.client.post(EDIT_ENDPOINT, data={
            "title": "TestSubforum", "description": "Updated description"})
        self.assertIn(
            b'{"msg":"Subforum updated"}',
            res.data, "Successful response")
