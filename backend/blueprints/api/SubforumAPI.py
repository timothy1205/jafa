from flask import request, session

from backend.blueprints.AbstractBlueprintWrapper import AbstractBlueprintWrapper
from backend.blueprints.api.UserAPI import require_logged_in
from backend.constants import DATA
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.SubForumManager import (
    InvalidSubForumDescription,
    InvalidSubForumTitle,
    NoSubForumFoundError,
    RolePermissionError,
    SubForumTitleExistsError,
)
from backend.utils import make_error, make_success, require_keys


class SubforumAPI(AbstractBlueprintWrapper):
    def __init__(self, manager_factory: type[AbstractManagerFactory] | None = None):
        super().__init__("subforum", __name__, manager_factory=manager_factory)

        self.route("/create", self.create, methods=["POST"])
        self.route("/delete", self.delete, methods=["DELETE"])
        self.route("/edit", self.edit, methods=["POST"])

    @require_keys(["title", "description"])
    @require_logged_in
    def create(self):
        """
        ###**POST /api/subforum/create**

        Create a subforum.

        > title: Subforum title
        >
        > description: Subforum description

        ###Error Types:
        * InvalidSubForumDescription
        * InvalidSubForumTitle
        * SubForumTitleExistsError
        """
        title = request.form.get("title")
        description = request.form.get("description")
        creator = session[DATA.USER]["username"]

        subforum_manager = self.manager_factory.create_subforum_manager()
        try:
            created = subforum_manager.create_subforum(creator, title, description)
        except (
            InvalidSubForumDescription,
            InvalidSubForumTitle,
            SubForumTitleExistsError,
        ) as e:
            return make_error(str(e), e=e)
        if not created:
            return make_error("Could not create")
        return make_success("Subforum created")

    @require_keys(["title"])
    @require_logged_in
    def delete(self):
        """
        ###**POST /api/subforum/delete**

        Delete a subforum.

        > title: Subforum title

        ###Error Types:
        * NoSubForumFoundError
        * RolePermissionError
        """

        title = request.form.get("title")
        username = session[DATA.USER]["username"]

        subforum_manager = self.manager_factory.create_subforum_manager()
        try:
            deleted = subforum_manager.delete_subforum(username, title)
        except (NoSubForumFoundError, RolePermissionError) as e:
            return make_error(str(e), e=e)
        if not deleted:
            return make_error("Could not delete")

        return make_success("Subforum deleted")

    @require_keys(["title", "description"])
    @require_logged_in
    def edit(self):
        """
        ###**POST /api/subforum/edit**

        Edit a subforum.

        > title: Subforum title
        >
        > description: Subforum description

        ###Error Types:
        * NoSubForumFoundError
        * RolePermissionError
        """

        title = request.form.get("title")
        description = request.form.get("description")
        username = session[DATA.USER]["username"]

        subforum_manager = self.manager_factory.create_subforum_manager()
        try:
            updated = subforum_manager.edit_subforum(username, title, description)
        except (NoSubForumFoundError, RolePermissionError) as e:
            return make_error(str(e), e=e)
        if not updated:
            return make_error("Could not update subforum")

        return make_success("Subforum updated")
