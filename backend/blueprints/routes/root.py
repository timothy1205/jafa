from flask import Blueprint, session
from backend.blueprints.user import USER_NAME

from backend.data.managers.PostMananger import PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.utils import make_success

ROOT_NAME = "/"

blueprint = Blueprint(ROOT_NAME, __name__, url_prefix=ROOT_NAME)


@blueprint.route("/")
def root():
    post_manager = PostManager()
    subforum_manager = SubForumManager()

    posts = post_manager.get_post_list()
    # TODO: Indicate if a user liked/disliked a post

    info = subforum_manager.get_subforum_info()

    return make_success(dict(posts=posts, info=info))
