from backend.blueprints.AbstractBlueprintManager import AbstractBlueprintManager
from backend.blueprints.routes.PostRoute import PostRoute
from backend.blueprints.routes.RootRoute import RootRoute
from backend.blueprints.routes.SubforumRoute import SubforumRoute


class RouteBlueprintManager(AbstractBlueprintManager):
    def __init__(self):
        super().__init__("route", __name__)

        self.get_blueprint().register_blueprint(PostRoute().blueprint)
        self.get_blueprint().register_blueprint(RootRoute().blueprint)
        self.get_blueprint().register_blueprint(SubforumRoute().blueprint)
