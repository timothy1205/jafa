import unittest

from backend.app import create_app
from backend.blueprints.routes.PostRoute import PostRoute
from backend.data.managers.PostMananger import NoPostFoundError
from backend.tests.blueprints import TestManagerFactory, setup_test_context
from backend.tests.blueprints.api.PostAPI_test import TestPostManager


class PostRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()

        self.test_manager_factory = TestManagerFactory()

        self.post_manger = TestPostManager()
        self.test_manager_factory.create_post_manager = lambda: self.post_manger

        self.post_route = PostRoute(manager_factory=self.test_manager_factory)

    def test_post(self):
        with self.subTest("Invalid post"):

            def test():
                def raise_e(post_id):
                    raise NoPostFoundError()

                self.post_manger.get_post = raise_e

                response = self.post_route.post("").get_json()

                self.assertIn("type", response)
                self.assertEqual("NoPostFoundError", response["type"])

                self.assertIn("error", response)
                self.assertIsInstance(response["error"], str)

            setup_test_context(self.app, test)

        with self.subTest("Post returned"):

            def test():
                test_data = dict(title="Test Post", body="Test Post")

                self.post_manger.get_post = lambda post_id: test_data

                response = self.post_route.post("").get_json()

                self.assertEqual(test_data, response)

            setup_test_context(self.app, test)
