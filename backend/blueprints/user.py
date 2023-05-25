from flask import Blueprint, request, make_response, jsonify
from backend.utils import make_error, make_success
from backend.databases.data.UserManager import UserManager, UsernameExistsError, InvalidUsernameError, InvalidPasswordError

USER_NAME = "user"
USER_PATH = f"/{USER_NAME}"
CODE_UNAUTHORIZED = 401

blueprint = Blueprint(USER_NAME, __name__,
                      url_prefix=USER_PATH)


@blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_manager = UserManager()
    valid_password = user_manager.check_password(username, password)

    if not valid_password:
        return make_error("Invalid credentials", CODE_UNAUTHORIZED)

    return "OK"


@blueprint.route("/register", methods=["POST"])
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

    return "OK"
