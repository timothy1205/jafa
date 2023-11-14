from functools import wraps

from flask import request, session

from backend.blueprints.AbstractBlueprintWrapper import AbstractBlueprintWrapper
from backend.constants import DATA, HTTP
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.UserManager import (
    InvalidPasswordError,
    InvalidUsernameError,
    UsernameExistsError,
)
from backend.utils import make_error, make_success, require_keys


class NotLoggedIn(Exception):
    """Indicate a user isn't logged in."""

    pass


class AlreadyLoggedIn(Exception):
    """Indicate a user is already logged in."""

    pass


def require_logged_in(f):
    """Decorator: Ensure endpoint caller is logged in."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if DATA.USER not in session:
            return make_error("You must be logged in", HTTP.UNAUTHORIZED, NotLoggedIn())

        return f(*args, **kwargs)

    return wrapper


class UserAPI(AbstractBlueprintWrapper):
    def __init__(self, manager_factory: type[AbstractManagerFactory] | None = None):
        super().__init__("user", __name__, manager_factory=manager_factory)

        self.route("/login", self.login, methods=["POST"])
        self.route("/logout", self.logout)
        self.route("/register", self.register, methods=["POST"])
        self.route("/get", self.get)

    @require_keys(["username", "password"])
    def login(self):
        if DATA.USER in session:
            return make_error("Already logged in", HTTP.UNAUTHORIZED)

        username = request.form.get("username")
        password = request.form.get("password")

        user_manager = self.manager_factory.create_user_manager()
        valid_password, user = user_manager.check_password(username, password)

        if not valid_password:
            return make_error(
                "Invalid credentials", HTTP.UNAUTHORIZED, AlreadyLoggedIn()
            )

        session[DATA.USER] = user
        return make_success("Logged in")

    @require_logged_in
    def logout(self):
        session.clear()
        return make_success("Logged out")

    @require_keys(["username", "password"])
    def register(self):
        username = request.form.get("username")
        password = request.form.get("password")

        user_manager = self.manager_factory.create_user_manager()

        try:
            user = user_manager.create_user(username, password)
        except (UsernameExistsError, InvalidUsernameError, InvalidPasswordError) as e:
            return make_error(str(e), HTTP.UNAUTHORIZED, e)
        if user is None:
            return make_error("Could not create!", HTTP.UNAUTHORIZED)

        # Treat new user as logged in
        session[DATA.USER] = user
        return make_success("User created")

    def get(self):
        if DATA.USER not in session:
            return make_success({})

        user = session[DATA.USER]

        return make_success(
            dict(registration_date=user["registration_date"], username=user["username"])
        )
