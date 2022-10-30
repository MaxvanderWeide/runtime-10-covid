from flask import make_response, jsonify, Response

from openapi_server.storage_mock.storage_client import get_client


class DataController:
    def __init__(self):
        self.s_client = get_client()

    def get_cases(self):
        raise NotImplementedError

    def get_deaths(self):
        raise NotImplementedError

    def get_policies(self):
        raise NotImplementedError

    def get_temperatures(self):
        raise NotImplementedError

    def get_vaccinations(self):
        raise NotImplementedError


def get_cases() -> Response:
    return make_response(jsonify(DataController().get_cases()))


def get_deaths() -> Response:
    return make_response(jsonify(DataController().get_deaths()))


def get_policies() -> Response:
    return make_response(jsonify(DataController().get_policies()))


def get_temperatures() -> Response:
    return make_response(jsonify(DataController().get_temperatures()))


def get_vaccinations() -> Response:
    return make_response(jsonify(DataController().get_vaccinations()))
