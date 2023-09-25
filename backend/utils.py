from functools import wraps

from flask import Blueprint, jsonify, make_response, request

from .constants import HTTP


class RolePermissionError(Exception):
    def __init__(self, message="Insufficient permissions"):
        self.message = message


class MissingKeysError(Exception):
    pass


class ActionFailed(Exception):
    pass


def make_error(msg: str, code: int = HTTP.BAD_REQUEST, e: Exception = ActionFailed()):
    response = make_response(
        jsonify({"type": e.__class__.__name__, "error": msg}), code
    )
    response.headers["Content-Type"] = "application/json"

    return response


def make_success(data: str | dict):
    response_data = {"msg": data} if type(data) is str else data
    response = make_response(jsonify(response_data), HTTP.SUCCESS)
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
                    HTTP.BAD_REQUEST,
                    MissingKeysError(),
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator


def ceil_division(a: int, b: int):
    return -(a // -b)


def make_blueprint(name: str, import_name: str, url_prefix: str | None = None):
    """Return a blueprint with a given name.

    Url prefix defaults to "/<name>" if missing/empty.
    """
    if url_prefix is None:
        url_prefix = f"/{name}"

    return Blueprint(name, import_name, url_prefix=url_prefix)
