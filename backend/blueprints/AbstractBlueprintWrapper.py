from abc import ABC
from typing import Type

from flask.typing import RouteCallable
from backend.data.managers.ManagerFactory import ManagerFactory

from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.utils import make_blueprint


class AbstractBlueprintWrapper(ABC):
    """Wrapper class for implenting api/route endpoints.

    :param: manager_factory: The backend.data.managers.AbstractManagerFactory to use.
    A value of None will create a backend.data.managers.ManagerFactory object.
    """

    def __init__(
        self,
        name: str,
        import_name: str,
        url_prefix: str | None = None,
        manager_factory: Type[AbstractManagerFactory] | None = None,
    ):
        if manager_factory is None:
            self.manager_factory = ManagerFactory()
        else:
            self.manager_factory = manager_factory

        self.blueprint = make_blueprint(name, import_name, url_prefix)

    def route(self, rule: str, f: RouteCallable, **options):
        """Recreate the blueprint.route decorator for our class."""

        endpoint = options.pop("endpoint", None)
        self.blueprint.add_url_rule(rule, endpoint, f, **options)
