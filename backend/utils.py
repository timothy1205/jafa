from functools import wraps

from flask import g, jsonify, make_response, request

CODE_BAD_REQUEST = 400
CODE_SUCCESS = 200


class RolePermissionError(Exception):
    def __init__(self, message="Insufficient permissions"):
        self.message = message


class MissingKeysError(Exception):
    pass


class ActionFailed(Exception):
    pass


def make_error(msg: str, code: int, e: Exception = ActionFailed()):
    response = make_response(
        jsonify({"type": e.__class__.__name__, "error": msg}), code
    )
    response.headers["Content-Type"] = "application/json"

    return response


def make_success(data: str | dict):
    response_data = {"msg": data} if type(data) is str else data
    response = make_response(jsonify(response_data), CODE_SUCCESS)
    response.headers["Content-Type"] = "application/json"

    return response


def require_keys(keys: list[str]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            copy = list(keys)
            for key in keys:
                if key in request.values:
                    copy.remove(key)

            if len(copy) > 0:
                return make_error(
                    f"Missing: {str(sorted(copy))}",
                    CODE_BAD_REQUEST,
                    MissingKeysError(),
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def ceil_division(a: int, b: int):
    return -(a // -b)
