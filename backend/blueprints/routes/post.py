from backend.data.managers.PostMananger import NoPostFoundError, PostManager
from backend.utils import make_blueprint, make_error, make_success

blueprint = make_blueprint("post", __name__)


@blueprint.route("/<post_id>/")
def post(post_id: str):
    post_manager = PostManager()

    try:
        post = post_manager.get_post(post_id)
    except NoPostFoundError as e:
        return make_error(str(e), e=e)

    return make_success(post)
