from flask import make_response, jsonify, Response

from storage_mock.storage_client import get_client


class DataController:
    def __init__(self):
        self.s_client = get_client()


    def post_stores(self, body):
        self.s_client.append_entity("covid", body)
        return make_response("Stores stored", 201)

    def get_cases(self):
        data = self.s_client.get_entity('covid')["data"]['cases']
        response = []
        for country in data:
            series = []
            for i in data[country]:
                series.append(
                    {
                        "name": i,
                        "value": data[country][i]["total_cases"] or 0
                    }
                )
            response.append(
                {
                    "name": country,
                    "series": series
                }
            )
        return response


    def get_deaths(self):
        data = self.s_client.get_entity('covid')["data"]['deaths']
        response = []
        for country in data:
            series = []
            for i in data[country]:
                series.append(
                    {
                        "name": i,
                        "value": data[country][i]["total_deaths"] or 0
                    }
                )
            response.append(
                {
                    "name": country,
                    "series": series
                }
            )
        return response

    def get_policies(self):
        raise NotImplementedError

    def get_temperatures(self):
        raise NotImplementedError

    def get_vaccinations(self):
        data = self.s_client.get_entity('covid')["data"]['vaccinations']
        response = []
        for country in data:
            series = []
            for i in data[country]:
                series.append(
                    {
                        "name": i,
                        "value": data[country][i]["total_vaccinations"] or 0
                    }
                )
            response.append(
                {
                    "name": country,
                    "series": series
                }
            )
        return response


def post_stores(body) -> Response:
    return DataController().post_stores(body)


def get_cases() -> Response:
    return make_response(jsonify(DataController().get_cases()), 200)


def get_deaths() -> Response:
    return make_response(jsonify(DataController().get_deaths()), 200)


def get_policies() -> Response:
    return make_response(jsonify(DataController().get_policies()), 200)


def get_temperatures() -> Response:
    return make_response(jsonify(DataController().get_temperatures()), 200)


def get_vaccinations() -> Response:
    return make_response(jsonify(DataController().get_vaccinations()), 200)
