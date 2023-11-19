from backend.blueprints.api.SubforumAPI import SubforumAPI
from backend.data.managers.SubForumManager import (
    InvalidSubForumDescription,
    InvalidSubForumTitle,
    NoSubForumFoundError,
    SubForumInfoGeneric,
    SubForumInfoSpecific,
    SubForumManager,
    SubForumTitleExistsError,
)
from backend.data.models.SubForumModel import SubForum
from backend.tests.blueprints import (
    BlueprintTestCase,
    blueprint_test_fail,
    blueprint_test_raise,
    blueprint_test_success,
)
from backend.utils import RolePermissionError


class TestSubForumManager(SubForumManager):
    def get_subforum(self, title: str) -> SubForum:  # NOSONAR
        pass

    def create_subforum(
        self, creator: str, title: str, description: str
    ) -> bool:  # NOSONAR
        pass

    def delete_subforum(self, username: str, title: str) -> bool:  # NOSONAR
        pass

    def edit_subforum(
        self, username: str, title: str, description: str
    ) -> bool:  # NOSONAR
        pass

    def get_subforum_info(
        self,
        title: str | None = None,
        current_page: int = 0,
        page_limit: int | None = None,
    ) -> SubForumInfoGeneric | SubForumInfoSpecific:  # NOSONAR
        pass


class SubForumEndpointTestCase(BlueprintTestCase):
    def setUp(self):
        super().setUp()

        self.subforum_manager = TestSubForumManager()
        self.test_manager_factory.create_subforum_manager = (
            lambda: self.subforum_manager
        )

        self.subforum_api = SubforumAPI(manager_factory=self.test_manager_factory)

    def test_create(self):
        run = self.subforum_api.create
        request_data = dict(title="", description="")
        method = "create_subforum"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Subforum created",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Could not create",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            [
                InvalidSubForumDescription,
                InvalidSubForumTitle,
                SubForumTitleExistsError,
            ],
        )

    def test_delete(self):
        run = self.subforum_api.delete
        request_data = dict(title="")
        method = "delete_subforum"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Subforum deleted",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Could not delete",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            [NoSubForumFoundError, RolePermissionError],
        )

    def test_edit(self):
        run = self.subforum_api.edit
        request_data = dict(title="", description="")
        method = "edit_subforum"
        blueprint_test_success(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Subforum updated",
        )

        blueprint_test_fail(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            "Could not update subforum",
        )

        blueprint_test_raise(
            self,
            self.app,
            run,
            request_data,
            self.subforum_manager,
            method,
            [NoSubForumFoundError, RolePermissionError],
        )
