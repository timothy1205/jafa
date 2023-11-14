from backend.blueprints.AbstractBlueprintManager import AbstractBlueprintManager
from backend.blueprints.api.PostAPI import PostAPI
from backend.blueprints.api.SubforumAPI import SubforumAPI
from backend.blueprints.api.UserAPI import UserAPI


class APIBlueprintManager(AbstractBlueprintManager):
    def __init__(self):
        super().__init__("api", __name__)

        self.get_blueprint().register_blueprint(PostAPI().blueprint)
        self.get_blueprint().register_blueprint(SubforumAPI().blueprint)
        self.get_blueprint().register_blueprint(UserAPI().blueprint)
