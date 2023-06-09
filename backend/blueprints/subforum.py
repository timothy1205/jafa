from flask import Blueprint, request, session
from functools import wraps
from backend.utils import make_error, make_success, require_form_keys
from backend.databases.data.SubForumManager import \
    SubForumManager, InvalidDescriptionError, InvalidTitleError, TitleExistsError, NoTitleFoundError, RolePermissionError, UnchangedDescriptionError
from backend.blueprints.user import require_logged_in, USER_NAME

SUBFORUM_NAME = "subforum"
SUBFORUM_PATH = f"/{SUBFORUM_NAME}"
CODE_BAD_REQUEST = 400

blueprint = Blueprint(SUBFORUM_NAME, __name__,
                      url_prefix=SUBFORUM_PATH)


@blueprint.route("/create", methods=["POST"])
@require_form_keys(["title", "description"])
@require_logged_in
def create():
    title = request.form.get("title")
    description = request.form.get("description")
    creator = session[USER_NAME]["username"]

    subforum_manager = SubForumManager()
    try:
        created = subforum_manager.create_subforum(
            creator, title, description)
    except (InvalidDescriptionError, InvalidTitleError, TitleExistsError) as e:
        return make_error(str(e), CODE_BAD_REQUEST)
    if not created:
        return make_error("Could not create", CODE_BAD_REQUEST)
    return make_success("Subforum created")


@blueprint.route("/delete", methods=["DELETE"])
@require_form_keys(["title"])
@require_logged_in
def delete():
    title = request.form.get("title")
    username = session[USER_NAME]["username"]

    subforum_manager = SubForumManager()
    try:
        deleted = subforum_manager.delete_subforum(username, title)
    except (NoTitleFoundError, RolePermissionError) as e:
        return make_error(str(e), CODE_BAD_REQUEST)
    if not deleted:
        return make_error("Could not delete", CODE_BAD_REQUEST)

    return make_success("Subforum deleted")


@blueprint.route("/edit", methods=["POST"])
@require_form_keys(["title", "description"])
@require_logged_in
def edit():
    title = request.form.get("title")
    description = request.form.get("description")
    username = session[USER_NAME]["username"]

    subforum_manager = SubForumManager()
    try:
        updated = subforum_manager.edit_subforum(username, title, description)
    except (NoTitleFoundError, UnchangedDescriptionError, RolePermissionError) as e:
        return make_error(str(e), CODE_BAD_REQUEST)
    if not updated:
        return make_error("Could not update subforum", CODE_BAD_REQUEST)

    return make_success("Subforum updated")
