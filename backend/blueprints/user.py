from flask import Blueprint, request, make_response, jsonify, session
from functools import wraps
from backend.utils import make_error, make_success
from backend.databases.data.UserManager import UserManager, UsernameExistsError, InvalidUsernameError, InvalidPasswordError

USER_NAME = "user"
USER_PATH = f"/{USER_NAME}"
CODE_BAD_REQUEST = 400
CODE_UNAUTHORIZED = 401
CODE_CONFLICT = 409

blueprint = Blueprint(USER_NAME, __name__,
                      url_prefix=USER_PATH)


def require_credentials(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in request.form \
                or "password" not in request.form:
            return make_error("Missing username and/or password", CODE_BAD_REQUEST)

        return f(*args, **kwargs)
    return wrapper


def require_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if USER_NAME not in session:
            return make_error("You must be logged in", CODE_UNAUTHORIZED)

        return f(*args, **kwargs)
    return wrapper


@blueprint.route("/login", methods=["POST"])
@require_credentials
def login():
    if USER_NAME in session:
        return make_error("Already logged in", CODE_CONFLICT)

    username = request.form.get("username")
    password = request.form.get("password")

    user_manager = UserManager()
    valid_password, user = user_manager.check_password(username, password)

    if not valid_password:
        return make_error("Invalid credentials", CODE_UNAUTHORIZED)

    session[USER_NAME] = user
    return make_success("Logged in")


@blueprint.route("/register", methods=["POST"])
@require_credentials
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    user_manager = UserManager()

    try:
        created = user_manager.create_user(username, password)
    except (UsernameExistsError, InvalidUsernameError, InvalidPasswordError) as e:
        return make_error(str(e), CODE_UNAUTHORIZED)
    if not created:
        return make_error("Could not create!", CODE_UNAUTHORIZED)

    return make_success("User created")
