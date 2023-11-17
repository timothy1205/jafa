import unittest

from backend.app import create_app
from backend.blueprints.routes.RootRoute import RootRoute
from backend.data.managers.PostMananger import InvalidPageError
from backend.tests.blueprints import TestManagerFactory, setup_test_context
from backend.tests.blueprints.api.PostAPI_test import TestPostManager
from backend.tests.blueprints.api.SubforumAPI_test import TestSubForumManager


class RootRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()

        self.test_manager_factory = TestManagerFactory()

        self.post_manger = TestPostManager()
        self.test_manager_factory.create_post_manager = lambda: self.post_manger

        self.subforum_manager = TestSubForumManager()
        self.test_manager_factory.create_subforum_manager = (
            lambda: self.subforum_manager
        )

        self.root_route = RootRoute(manager_factory=self.test_manager_factory)

    def test_root(self):
        with self.subTest("Invalid page number"):

            def test():
                def raise_e(subforum, page=0, page_limit=None):
                    raise InvalidPageError()

                self.post_manger.get_post_list = raise_e

                response = self.root_route.root().get_json()

                self.assertIn("type", response)
                self.assertEqual("InvalidPageError", response["type"])

                self.assertIn("error", response)
                self.assertIsInstance(response["error"], str)

            setup_test_context(self.app, test)

        with self.subTest("Successful request"):

            def test():
                test_post_data = [
                    dict(title="Test Post", body="Test Post"),
                    dict(title="Test Post 2", body="Test Post 2"),
                ]

                test_info_data = dict(post_count=5, page_count=1, current_page=1)

                self.post_manger.get_post_list = (
                    lambda subforum, page=0, page_limit=None: test_post_data
                )
                self.subforum_manager.get_subforum_info = (
                    lambda title=None, current_page=0, page_limit=None: test_info_data
                )

                response = self.root_route.root().get_json()

                self.assertEqual(test_post_data, response["posts"])
                self.assertEqual(test_info_data, response["info"])

            setup_test_context(self.app, test)
