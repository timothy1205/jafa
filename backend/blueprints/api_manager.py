import os.path

from backend.blueprints.BlueprintManager import BlueprintManager

import_path = os.path.join(os.path.dirname(__file__), "api")
api_manager = BlueprintManager("api", __name__, import_path)
