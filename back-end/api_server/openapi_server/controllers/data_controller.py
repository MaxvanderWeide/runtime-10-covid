import datetime
import dateutil.relativedelta

from flask import make_response, jsonify, Response

from storage_mock.storage_client import get_client


class DataController:
    def __init__(self):
        self.s_client = get_client()

    def post_stores(self, body):
        self.s_client.append_entity("covid", body)
        return make_response("Stores stored", 201)

    def get_data(self, entity, value, v='data'):
        data = self.s_client.get_entity('covid')[v][entity]
        response = []
        for country in data:
            series = []
            for i in data[country]:
                series.append(
                    {
                        "name": i,
                        "value": data[country][i][value] or 0
                    }
                )
            response.append(
                {
                    "name": country,
                    "series": series
                }
            )
        return response

    def get_predictor(self):
        data = self.s_client.get_entity('covid')['data']['cases']
        lstmn = (datetime.datetime.today() - dateutil.relativedelta.relativedelta(months=3)).strftime('%Y-%m-%d')
        response = []
        for country in data:
            series = []
            for i in data[country]:
                if i < lstmn:
                    continue
                series.append(
                    {
                        "name": i,
                        "value": data[country][i]['new_cases'] or 0
                    }
                )
            response.append(
                {
                    "name": country,
                    "series": series
                }
            )
        for country in self.s_client.get_entity('covid')['forecast']['cases']['RFR_new_cases_A']:
            series = []
            for d in self.s_client.get_entity('covid')['forecast']['cases']['RFR_new_cases_A'][country]:
                if d == 'parameters':
                    continue
                series.append(
                    {
                        "name": d,
                        "value": self.s_client.get_entity('covid')['forecast']['cases']['RFR_new_cases_A'][country][d]['new_cases'] or 0
                    }
                )
            response.append(
                {
                    "name": country + '_new',
                    "series": series
                }
            )
        return response

    def get_cases(self):
        return self.get_data('cases', 'total_cases')

    def get_deaths(self):
        return self.get_data('deaths', 'total_deaths')

    def get_policies(self):
        raise NotImplementedError

    def get_temperatures(self):
        raise NotImplementedError

    def get_vaccinations(self):
        return self.get_data('vaccinations', 'total_vaccinations')

    def get_cases_new(self):
        return self.get_data('cases', 'new_cases')

    def get_deaths_new(self):
        return self.get_data('deaths', 'new_deaths')

    def get_vaccinations_new(self):
        return self.get_data('vaccinations', 'new_vaccinations')


def post_stores(body) -> Response:
    return DataController().post_stores(body)


def get_cases() -> Response:
    return make_response(jsonify(DataController().get_cases()), 200)


def get_predictor() -> Response:
    return make_response(jsonify(DataController().get_predictor()), 200)


def get_deaths() -> Response:
    return make_response(jsonify(DataController().get_deaths()), 200)


def get_policies() -> Response:
    return make_response(jsonify(DataController().get_policies()), 200)


def get_temperatures() -> Response:
    return make_response(jsonify(DataController().get_temperatures()), 200)


def get_vaccinations() -> Response:
    return make_response(jsonify(DataController().get_vaccinations()), 200)


def get_cases_new() -> Response:
    return make_response(jsonify(DataController().get_cases_new()), 200)


def get_deaths_new() -> Response:
    return make_response(jsonify(DataController().get_deaths_new()), 200)


def get_vaccinations_new() -> Response:
    return make_response(jsonify(DataController().get_vaccinations_new()), 200)
