from flask import make_response, jsonify


def make_error(msg: str, code: int):
    response = make_response(jsonify({"error": msg}), code)
    response.headers["Content-Type"] = "application/json"

    return response


def make_success(msg: str, code=200):
    response = make_response(jsonify({"msg": msg}), code)
    response.headers["Content-Type"] = "application/json"
