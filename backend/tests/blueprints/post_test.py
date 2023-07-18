import unittest

from flask import g

from backend.app import create_app
from backend.JafaConfig import JafaConfig
from backend.tests.blueprints.user_test import login, register
from backend.tests.data.models.TestModelFactory import TestModelFactory
from backend.tests.blueprints.subforum_test import create_subforum

CREATE_ENDPOINT = "/api/post/create"
DELETE_ENDPOINT = "/api/post/delete"
EDIT_ENDPOINT = "/api/post/edit"
LOCK_ENDPOINT = "/api/post/lock"
UNLOCK_ENDPOINT = "/api/post/unlock"
VOTE_ENDPOINT = "/api/post/vote"
UNVOTE_ENDPOINT = "/api/post/unvote"


def create_post(client, subforum, title, body):
    return client.post(
        CREATE_ENDPOINT, data=dict(subforum=subforum, title=title, body=body)
    )


class PostEndpointTestCase(unittest.TestCase):
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
            b'"type":"MissingKeysError"',
            res.data,
            "Erroneous response",
        )

        create_subforum(self.client, "TestSubforum", "Test subforum")
        res = create_post(self.client, "TestSubforum", "TestPost", "Test Message")
        self.assertIn(b'{"msg":"Post created"}', res.data, "Successful response")

    def test_delete(self):
        register(self.client, "red", "Password1")
        login(self.client, "red", "Password1")

        create_subforum(self.client, "TestSubforum", "Test subforum")
        create_post(self.client, "TestSubforum", "TestPost", "Test Message")

        res = self.client.delete(DELETE_ENDPOINT)
        self.assertIn(
            b'"type":"MissingKeysError"',
            res.data,
            "Erroneous response",
        )

        res = self.client.delete(DELETE_ENDPOINT, data=dict(post_id=0))
        self.assertIn(b'{"msg":"Post deleted"}', res.data, "Successful response")

    def test_edit(self):
        register(self.client, "red", "Password1")
        login(self.client, "red", "Password1")

        create_subforum(self.client, "TestSubforum", "Test subforum")
        create_post(self.client, "TestSubforum", "TestPost", "Test Message")

        res = self.client.post(EDIT_ENDPOINT)
        self.assertIn(
            b'"type":"MissingKeysError"',
            res.data,
            "Erroneous response",
        )

        res = self.client.post(
            EDIT_ENDPOINT, data=dict(post_id=0, title="New Title", body="New Message")
        )
        self.assertIn(b'{"msg":"Post updated"}', res.data, "Successful response")
