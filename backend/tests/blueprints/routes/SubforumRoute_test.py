from backend.blueprints.routes.SubforumRoute import SubforumRoute
from backend.data.managers.PostMananger import InvalidPageError
from backend.data.managers.SubForumManager import NoSubForumFoundError
from backend.tests.blueprints import (
    BlueprintTestCase,
    blueprint_test_raise,
    setup_test_context,
)
from backend.tests.blueprints.api.PostAPI_test import TestPostManager
from backend.tests.blueprints.api.SubforumAPI_test import TestSubForumManager


class SubForumRouteTestCase(BlueprintTestCase):
    def setUp(self):
        super().setUp()

        self.post_manger = TestPostManager()
        self.test_manager_factory.create_post_manager = lambda: self.post_manger

        self.subforum_manager = TestSubForumManager()
        self.test_manager_factory.create_subforum_manager = (
            lambda: self.subforum_manager
        )

        self.subforum_route = SubforumRoute(manager_factory=self.test_manager_factory)

    def test_subforum(self):
        blueprint_test_raise(
            self,
            self.app,
            self.subforum_route.subforum,
            None,
            self.post_manger,
            "get_post_list",
            [InvalidPageError],
        )

        blueprint_test_raise(
            self,
            self.app,
            self.subforum_route.subforum,
            None,
            self.subforum_manager,
            "get_subforum_info",
            [NoSubForumFoundError],
        )

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

                response = self.subforum_route.subforum().get_json()

                self.assertEqual(test_post_data, response["posts"])
                self.assertEqual(test_info_data, response["info"])

            setup_test_context(self.app, test)
