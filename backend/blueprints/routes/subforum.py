from backend.data.managers.PostMananger import InvalidPageError, PostManager
from backend.data.managers.SubForumManager import NoSubForumFoundError, SubForumManager
from backend.utils import make_blueprint, make_error, make_success

blueprint = make_blueprint("subforum", __name__)
CODE_BAD_REQUST = 400


@blueprint.route("/<title>/")
@blueprint.route("/<title>/<int:page>")
def subforum(title: str | None = None, page: int = 0):
    post_manager = PostManager()
    subforum_manager = SubForumManager()

    try:
        info = subforum_manager.get_subforum_info(title, page)
        posts = post_manager.get_post_list(title, page)
    except (NoSubForumFoundError, InvalidPageError) as e:
        return make_error(str(e), CODE_BAD_REQUST, e)

    return make_success(dict(posts=posts, info=info))
