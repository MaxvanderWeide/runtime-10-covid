import json
from datetime import datetime

import pandas as pd
import requests
from flask import make_response, jsonify


class LiveController:

    def __init__(self):
        self.data = {}

    def fetch_norway(self):
        """
        Function to fetch data from government github reposity for Norway
        :return: Dictionary with date, hours, cases and deaths
        """
        data = pd.read_csv(
            'https://raw.githubusercontent.com/thohan88/covid19-nor-data/master/data/01_infected/msis/municipality_and_district.csv')
        date = str(datetime.strptime(data.iloc[-1:]['date_time'].values[0], "%Y-%m-%dT%H:%M:%SZ"))
        data = data[['date', 'cases']]
        hours = (datetime.strptime(data.date.unique()[-2:][1], "%Y-%m-%d") - datetime.strptime(data.date.unique()[-2:][0],
                                                                                               "%Y-%m-%d")).days * 24
        data = data.loc[data['date'].isin(data.date.unique()[-2:])]
        data = data.groupby('date')['cases'].sum()
        data = data.diff()
        cases = data.iloc[-1:][0]
        print(date)
        return {'date': date, 'hours': int(hours), 'cases': int(cases)}

    def fetch_netherlands(self):
        """
        Function to fetch data from government reposity at rivm.nl for the Netherlands
        :return: Dictionary with date, hours, cases and deaths
        """
        data = pd.read_csv('https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv', delimiter=";")
        date = str(data.iloc[-1:]['Date_of_report'].values[0])
        data = data[['Date_of_publication', 'Total_reported', 'Deceased']]
        hours = (datetime.strptime(data.Date_of_publication.unique()[-2:][1], "%Y-%m-%d") - datetime.strptime(
            data.Date_of_publication.unique()[-2:][0], "%Y-%m-%d")).days * 24
        data = data.loc[data['Date_of_publication'].isin(data.Date_of_publication.unique()[-1:])]
        cases = data.groupby('Date_of_publication')['Total_reported'].sum()
        cases = cases.iloc[-1:][0]
        deaths = data.groupby('Date_of_publication')['Deceased'].sum()
        deaths = deaths.iloc[-1:][0]
        return {'date': date, 'hours': int(hours), 'cases': int(cases), 'deaths': int(deaths)}

    def fetch_spain(self):
        """
        Function to fetch data from covid19api.com for Spain
        :return: Dictionary with date, hours, cases and deaths
        """
        return self._fetch_covid_19_api("https://api.covid19api.com/dayone/country/spain")

    def fetch_brazil(self):
        """
        Function to fetch data from covid19api.com for Brazil
        :return: Dictionary with date, hours, cases and deaths
        """
        return self._fetch_covid_19_api("https://api.covid19api.com/dayone/country/brazil")

    def _fetch_covid_19_api(self, url: str):
        """
        Helper function to fetch data from covid19api.com for a given country
        :param: url: URL to fetch data from
        :return: Dictionary with date, hours, cases and deaths
        """
        response = requests.request("GET", url, headers={}, data={})
        result = json.loads(response.text)
        result = result[-2:]
        hours = (datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(result[0]['Date'],
                                                                                                "%Y-%m-%dT%H:%M:%SZ")).days * 24
        date = str(datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
        cases = result[1]['Confirmed'] - result[0]['Confirmed']
        deaths = result[1]['Deaths'] - result[0]['Deaths']

        return {'date': date, 'hours': int(hours), 'cases': int(cases), 'deaths': int(deaths)}


def get_live(country):
    if country == 'norway':
        return make_response(jsonify(LiveController().fetch_norway()), 200)
    if country == 'brazil':
        return make_response(jsonify(LiveController().fetch_brazil()), 200)
    if country == 'netherlands':
        print(LiveController().fetch_netherlands())
        return make_response(jsonify(LiveController().fetch_netherlands()), 200)
    if country == 'spain':
        return make_response(jsonify(LiveController().fetch_spain()), 200)
    else:
        return make_response(jsonify("Not Found"), 404)
