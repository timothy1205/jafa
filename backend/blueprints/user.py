from functools import wraps

from flask import Blueprint, g, request, session

from backend.data.managers.UserManager import (
    InvalidPasswordError,
    InvalidUsernameError,
    UserManager,
    UsernameExistsError,
)
from backend.utils import CODE_BAD_REQUEST, make_error, make_success, require_keys


class NotLoggedIn(Exception):
    pass


class AlreadyLoggedIn(Exception):
    pass


USER_NAME = "user"
USER_PATH = f"/{USER_NAME}"
CODE_UNAUTHORIZED = 401
CODE_CONFLICT = 409

blueprint = Blueprint(USER_NAME, __name__, url_prefix=USER_PATH)


def require_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if USER_NAME not in session:
            return make_error("You must be logged in", CODE_UNAUTHORIZED, NotLoggedIn())

        return f(*args, **kwargs)

    return wrapper


@blueprint.route("/login", methods=["POST"])
@require_keys(["username", "password"])
def login():
    if USER_NAME in session:
        return make_error(
            "Already logged in",
            CODE_CONFLICT,
        )

    username = request.form.get("username")
    password = request.form.get("password")

    user_manager = UserManager()
    valid_password, user = user_manager.check_password(username, password)

    if not valid_password:
        return make_error("Invalid credentials", CODE_UNAUTHORIZED, AlreadyLoggedIn())

    session[USER_NAME] = user
    return make_success("Logged in")


@blueprint.route("/logout")
@require_logged_in
def logout():
    session.clear()
    return make_success("Logged out")


@blueprint.route("/register", methods=["POST"])
@require_keys(["username", "password"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    user_manager = UserManager()

    try:
        user = user_manager.create_user(username, password)
    except (UsernameExistsError, InvalidUsernameError, InvalidPasswordError) as e:
        return make_error(str(e), CODE_UNAUTHORIZED, e)
    if user is None:
        return make_error("Could not create!", CODE_UNAUTHORIZED)

    # Treat new user as logged in
    session[USER_NAME] = user
    return make_success("User created")


@blueprint.route("/get")
def get():
    if USER_NAME not in session:
        return make_success({})

    user = session[USER_NAME]

    return make_success(
        dict(registration_date=user["registration_date"], username=user["username"])
    )
