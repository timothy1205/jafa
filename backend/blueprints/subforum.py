from functools import wraps

from flask import request, session

from backend.blueprints.user import USER, require_logged_in
from backend.data.managers.SubForumManager import (
    InvalidSubForumDescription,
    InvalidSubForumTitle,
    NoSubForumFoundError,
    RolePermissionError,
    SubForumManager,
    SubForumTitleExistsError,
)
from backend.utils import make_blueprint, make_error, make_success, require_keys

CODE_BAD_REQUEST = 400

blueprint = make_blueprint("subforum", __name__)


@blueprint.route("/create", methods=["POST"])
@require_keys(["title", "description"])
@require_logged_in
def create():
    title = request.form.get("title")
    description = request.form.get("description")
    creator = session[USER]["username"]

    subforum_manager = SubForumManager()
    try:
        created = subforum_manager.create_subforum(creator, title, description)
    except (
        InvalidSubForumDescription,
        InvalidSubForumTitle,
        SubForumTitleExistsError,
    ) as e:
        return make_error(str(e), CODE_BAD_REQUEST, e)
    if not created:
        return make_error("Could not create", CODE_BAD_REQUEST)
    return make_success("Subforum created")


@blueprint.route("/delete", methods=["DELETE"])
@require_keys(["title"])
@require_logged_in
def delete():
    title = request.form.get("title")
    username = session[USER]["username"]

    subforum_manager = SubForumManager()
    try:
        deleted = subforum_manager.delete_subforum(username, title)
    except (NoSubForumFoundError, RolePermissionError) as e:
        return make_error(str(e), CODE_BAD_REQUEST, e)
    if not deleted:
        return make_error("Could not delete", CODE_BAD_REQUEST)

    return make_success("Subforum deleted")


@blueprint.route("/edit", methods=["POST"])
@require_keys(["title", "description"])
@require_logged_in
def edit():
    title = request.form.get("title")
    description = request.form.get("description")
    username = session[USER]["username"]

    subforum_manager = SubForumManager()
    try:
        updated = subforum_manager.edit_subforum(username, title, description)
    except (NoSubForumFoundError, RolePermissionError) as e:
        return make_error(str(e), CODE_BAD_REQUEST, e)
    if not updated:
        return make_error("Could not update subforum", CODE_BAD_REQUEST)

    return make_success("Subforum updated")
