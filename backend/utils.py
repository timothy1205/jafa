from functools import wraps

from flask import Blueprint, Response, jsonify, make_response, request

from .constants import HTTP


class RolePermissionError(Exception):
    """Indicate incorrect role for action."""

    def __init__(self, message="Insufficient permissions"):
        self.message = message


class MissingKeysError(Exception):
    """Indicate missing form keys/get parameters."""

    pass


class ActionFailed(Exception):
    """Indicate generic failure."""

    pass


def make_error(
    msg: str, code: int = HTTP.BAD_REQUEST, e: Exception = ActionFailed()
) -> Response:
    """Construct a Flask Response with an error message

    :return:
    ```
    {
    "type": Error type,
    "error" Error message
    }
    ```
    """
    response = make_response(
        jsonify({"type": e.__class__.__name__, "error": msg}), code
    )
    response.headers["Content-Type"] = "application/json"

    return response


def make_success(data: str | dict):
    """Construct a Flask Response for a piece of data

    :return:
    if type(data) is str:
    ```
    {
    "msg": Message
    }
    ```
    if type(data) is dict:

        data jsonified

    """
    response_data = {"msg": data} if type(data) is str else data
    response = make_response(jsonify(response_data), HTTP.SUCCESS)
    response.headers["Content-Type"] = "application/json"

    return response


def require_keys(keys: list[str]):
    """Decorator: Requires all keys to be present in request

    :return: Error response with MissingKeyError if check failed
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            copy = list(keys)
            for key in keys:
                if key in request.form:
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


def ceil_division(a: int, b: int) -> int:
    """Opposite of floor division"""
    return -(a // -b)


def make_blueprint(name: str, import_name: str, url_prefix: str | None = None):
    """Return a blueprint with a given name.

    Url prefix defaults to "/<name>" if missing/empty.
    """
    if url_prefix is None:
        url_prefix = f"/{name}"

    return Blueprint(name, import_name, url_prefix=url_prefix)


def set_data_wrapper(data: dict):
    """Return a set_data function with that updates the given data dict.

    Used in testing.
    """
    data["args"] = None
    data["kwargs"] = None

    def set_data(*args, **kwargs):
        data["args"] = args
        data["kwargs"] = kwargs

    return set_data
