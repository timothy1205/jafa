from flask import make_response, jsonify, request, g
from functools import wraps


CODE_BAD_REQUEST = 400


class RolePermissionError(Exception):
    def __init__(self, message="Insufficient permissions"):
        self.message = message


def make_error(msg: str, code: int):
    response = make_response(jsonify({"error": msg}), code)
    response.headers["Content-Type"] = "application/json"

    return response


def make_success(msg: str, code=200):
    response = make_response(jsonify({"msg": msg}), code)
    response.headers["Content-Type"] = "application/json"

    return response


def require_form_keys(keys: list[str]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            copy = list(keys)
            for key in keys:
                if key in request.form:
                    copy.remove(key)

            if len(copy) > 0:
                return make_error(f"Missing: {str(sorted(copy))}", CODE_BAD_REQUEST)

            return f(*args, **kwargs)
        return wrapper
    return decorator
