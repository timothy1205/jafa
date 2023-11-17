from backend.blueprints.AbstractBlueprintWrapper import AbstractBlueprintWrapper
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.PostMananger import NoPostFoundError
from backend.utils import make_error, make_success


class PostRoute(AbstractBlueprintWrapper):
    def __init__(self, manager_factory: type[AbstractManagerFactory] | None = None):
        super().__init__("post", __name__, manager_factory=manager_factory)

        self.route("/<post_id>/", self.post)

    def post(self, post_id: str):
        post_manager = self.manager_factory.create_post_manager()

        try:
            post = post_manager.get_post(post_id)
        except NoPostFoundError as e:
            return make_error(str(e), e=e)

        return make_success(post)
