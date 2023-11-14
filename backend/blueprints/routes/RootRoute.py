from backend.blueprints.AbstractBlueprintWrapper import AbstractBlueprintWrapper
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.PostMananger import InvalidPageError, PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.utils import make_blueprint, make_error, make_success

blueprint = make_blueprint("root", __name__, "/")


class RootRoute(AbstractBlueprintWrapper):
    def __init__(self, manager_factory: type[AbstractManagerFactory] | None = None):
        super().__init__("root", __name__, manager_factory=manager_factory)

        self.route("/<int:page>", self.root)
        self.route("/", self.root)

    def root(self, page: int = 0):
        post_manager = PostManager()
        subforum_manager = self.manager_factory.create_subforum_manager()

        try:
            posts = post_manager.get_post_list(page)
            # TODO: Indicate if a user liked/disliked a post
        except InvalidPageError as e:
            return make_error(str(e), e=e)

        info = subforum_manager.get_subforum_info(current_page=page)

        return make_success(dict(posts=posts, info=info))
