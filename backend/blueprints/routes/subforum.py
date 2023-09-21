from flask import Blueprint, session
from backend.blueprints.user import USER_NAME

from backend.data.managers.PostMananger import PostManager
from backend.data.managers.SubForumManager import NoSubForumFoundError, SubForumManager
from backend.utils import make_error, make_success

SUBFORUM_NAME = "subforum"
SUBFORUM_PATH = f"/{SUBFORUM_NAME}"


blueprint = Blueprint(SUBFORUM_NAME, __name__, url_prefix=SUBFORUM_PATH)
CODE_BAD_REQUST = 400


@blueprint.route("/<title>")
def subforum(title: str):
    post_manager = PostManager()
    subforum_manager = SubForumManager()

    try:
        info = subforum_manager.get_subforum_info(title)
        posts = post_manager.get_post_list(title)
    except NoSubForumFoundError as e:
        return make_error(str(e), CODE_BAD_REQUST, e)

    return make_success(dict(posts=posts, info=info))
