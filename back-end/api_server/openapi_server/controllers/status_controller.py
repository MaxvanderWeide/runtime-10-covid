from flask import make_response, jsonify, Response


class StatusController:
    def __init__(self):
        pass

    def get_status(self):
        return "OK"


def get_status() -> Response:
    return make_response(jsonify(StatusController().get_active_moves()), 200)