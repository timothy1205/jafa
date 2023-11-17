from backend.blueprints.AbstractBlueprintWrapper import AbstractBlueprintWrapper
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.PostMananger import InvalidPageError
from backend.data.managers.SubForumManager import NoSubForumFoundError
from backend.utils import make_error, make_success


class SubforumRoute(AbstractBlueprintWrapper):
    def __init__(self, manager_factory: type[AbstractManagerFactory] | None = None):
        super().__init__("subforum", __name__, manager_factory=manager_factory)

        self.route("/<title>/", self.subforum)
        self.route("/<title>/<int:page>", self.subforum)

    def subforum(self, title: str | None = None, page: int = 0):
        post_manager = self.manager_factory.create_post_manager()
        subforum_manager = self.manager_factory.create_subforum_manager()

        try:
            info = subforum_manager.get_subforum_info(title, page)
            posts = post_manager.get_post_list(title, page)
        except (NoSubForumFoundError, InvalidPageError) as e:
            return make_error(str(e), e=e)

        return make_success(dict(posts=posts, info=info))
