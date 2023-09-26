import os.path

from backend.blueprints.BlueprintManager import BlueprintManager

import_path = os.path.join(os.path.dirname(__file__), "routes")
route_manager = BlueprintManager("route", __name__, import_path)
