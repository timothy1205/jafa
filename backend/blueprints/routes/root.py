from flask import Blueprint, session
from backend.blueprints.user import USER_NAME

from backend.data.managers.PostMananger import InvalidPageError, PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.utils import make_error, make_success

ROOT_NAME = "/"

blueprint = Blueprint(ROOT_NAME, __name__, url_prefix=ROOT_NAME)
CODE_BAD_REQUST = 400


@blueprint.route("/<int:page>")
@blueprint.route("/")
def root(page: int = 0):
    post_manager = PostManager()
    subforum_manager = SubForumManager()

    try:
        posts = post_manager.get_post_list(page)
        # TODO: Indicate if a user liked/disliked a post
    except InvalidPageError as e:
        return make_error(str(e), CODE_BAD_REQUST, e)

    info = subforum_manager.get_subforum_info(current_page=page)

    return make_success(dict(posts=posts, info=info))
