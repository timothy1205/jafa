from flask import Blueprint, request, session
from functools import wraps
from backend.utils import make_error, make_success
from backend.databases.data.SubForumManager import SubForumManager, InvalidDescriptionError, InvalidTitleError, TitleExistsError
from backend.blueprints.user import require_logged_in, USER_NAME

SUBFORUM_NAME = "subforum"
SUBFORUM_PATH = f"/{SUBFORUM_NAME}"
CODE_BAD_REQUEST = 400

blueprint = Blueprint(SUBFORUM_NAME, __name__,
                      url_prefix=SUBFORUM_PATH)


@blueprint.route("/create", methods=["POST"])
@require_logged_in
def create():
    title = request.form.get("title")
    description = request.form.get("description")
    creator = session[USER_NAME]["username"]

    subforum_manager = SubForumManager()
    try:
        created = subforum_manager.create_subforum(
            session[USER_NAME], title, description)
    except (InvalidDescriptionError, InvalidTitleError, TitleExistsError) as e:
        return make_error(str(e), CODE_BAD_REQUEST)
    if not created:
        return make_error("Could not create!", CODE_BAD_REQUEST)
    return make_success("Subforum created")
