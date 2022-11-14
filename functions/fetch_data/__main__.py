from urllib.request import urlopen
import pandas as pd
import json
from pathlib import Path
from enum import Enum
from datetime import datetime, timedelta
import requests
from dateutil.parser import parse
import numpy as np
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor
from skforecast.model_selection import grid_search_forecaster
from sklearn.metrics import mean_squared_error

 
COUNTRIES = ["NLD", "BRA", "NOR", "ESP"]
ROOT = Path().parent.absolute()
STORAGE_FOLDER = ROOT / 'cleaned_data' / 'data'
FEATURES = {
    "demographics": ["population_density", "median_age", "aged_65_older", "aged_70_older", "cardiovasc_death_rate", "diabetes_prevalence", "female_smokers", "male_smokers", "handwashing_facilities", "hospital_beds_per_thousand", "life_expectancy", "human_development_index", "population", "reproduction_rate"],
    "economy": ["gdp_per_capita", "extreme_poverty"],
    "cases": ["total_cases", "new_cases", "new_cases_smoothed", "total_cases_per_million", "new_cases_per_million", "new_cases_smoothed_per_million"],
    "deaths": ["total_deaths", "new_deaths", "new_deaths_smoothed", "total_deaths_per_million", "new_deaths_per_million", "new_deaths_smoothed_per_million"],
    "tests": ["total_tests", "new_tests", "total_tests_per_thousand", "new_tests_per_thousand", "new_tests_smoothed", "new_tests_smoothed_per_thousand", "tests_per_case", "positive_rate", "tests_units"],
    "vaccinations": ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters", "new_vaccinations", "new_vaccinations_smoothed", "total_vaccinations_per_hundred", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "total_boosters_per_hundred", "new_vaccinations_smoothed_per_million", "new_people_vaccinated_smoothed", "new_people_vaccinated_smoothed_per_hundred"],
    "mortality": ["excess_mortality_cumulative_absolute", "excess_mortality_cumulative_per_million", "excess_mortality_cumulative", "excess_mortality"],
    "policy": ["stringency_index", "policy_facial_covering", "policy_school_closing", "policy_public_transport", "policy_gatherings_restriction", "policy_workplace_closing", "policy_travel_restriction"]
}

class Country(Enum):
    NORWAY = 1
    NETHERLANDS = 2
    SPAIN = 3
    BRAZIL = 4

class LiveDataFetcher:
    """
    Class for live fetching data from covid19api.com and government repositories
    """

    def __init__(self):
        self.data = {}

    def fetch_country(self, country: Country):
        """
        Function to fetch data from covid19api.com for a given country
        :param: country: Country to fetch data for, must be of type Country
        :return: Dictionary with date, hours, cases and deaths
        """
        if country == Country.NORWAY:
            return self._fetch_norway()
        elif country == Country.NETHERLANDS:
            return self._fetch_netherlands()
        elif country == Country.SPAIN:
            return self._fetch_spain()
        elif country == Country.BRAZIL:
            return self._fetch_brazil()
        else:
            raise ValueError("Country not supported")

    def _fetch_norway(self):
        """
        Function to fetch data from government github reposity for Norway
        :return: Dictionary with date, hours, cases and deaths
        """
        data = pd.read_csv('https://raw.githubusercontent.com/thohan88/covid19-nor-data/master/data/01_infected/msis/municipality_and_district.csv')
        date = str(datetime.strptime(data.iloc[-1:]['date_time'].values[0], "%Y-%m-%dT%H:%M:%SZ"))     
        data = data[['date', 'cases']]
        hours = (datetime.strptime(data.date.unique()[-2:][1], "%Y-%m-%d") - datetime.strptime(data.date.unique()[-2:][0], "%Y-%m-%d")).days * 24
        data = data.loc[data['date'].isin(data.date.unique()[-2:])]
        data = data.groupby('date')['cases'].sum()
        data = data.diff()
        cases = data.iloc[-1:][0]
        print(date)
        return {'date': date, 'hours': hours, 'cases': cases}

    def _fetch_netherlands(self):
        """
        Function to fetch data from government reposity at rivm.nl for the Netherlands
        :return: Dictionary with date, hours, cases and deaths
        """
        data = pd.read_csv('https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv', delimiter = ";")
        date = str(data.iloc[-1:]['Date_of_report'].values[0])
        data = data[['Date_of_publication', 'Total_reported', 'Deceased']]
        hours = (datetime.strptime(data.Date_of_publication.unique()[-2:][1], "%Y-%m-%d") - datetime.strptime(data.Date_of_publication.unique()[-2:][0], "%Y-%m-%d")).days * 24
        data = data.loc[data['Date_of_publication'].isin(data.Date_of_publication.unique()[-1:])]
        cases = data.groupby('Date_of_publication')['Total_reported'].sum()
        cases = cases.iloc[-1:][0]
        deaths = data.groupby('Date_of_publication')['Deceased'].sum()
        deaths = deaths.iloc[-1:][0]
        return {'date': date, 'hours': hours, 'cases': cases, 'deaths': deaths}

    def _fetch_spain(self):
        """
        Function to fetch data from covid19api.com for Spain
        :return: Dictionary with date, hours, cases and deaths
        """
        return self.__fetch_covid_19_api("https://api.covid19api.com/dayone/country/spain")

    def _fetch_brazil(self):
        """
        Function to fetch data from covid19api.com for Brazil
        :return: Dictionary with date, hours, cases and deaths
        """
        return self.__fetch_covid_19_api("https://api.covid19api.com/dayone/country/brazil")

    def __fetch_covid_19_api(self, url: str):
        """
        Helper function to fetch data from covid19api.com for a given country
        :param: url: URL to fetch data from
        :return: Dictionary with date, hours, cases and deaths
        """
        response = requests.request("GET", url, headers={}, data={})
        result = json.loads(response.text)
        result = result[-2:]
        hours = (datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(result[0]['Date'], "%Y-%m-%dT%H:%M:%SZ")).days * 24
        date = str(datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
        cases = result[1]['Confirmed'] - result[0]['Confirmed']
        deaths = result[1]['Deaths'] - result[0]['Deaths']

        return {'date': date, 'hours': hours, 'cases': cases, 'deaths': deaths}


class DataFetcher:
    """
    Class for fetching data from ourworldindata.com
    """

    def __init__(self):
        self.data = pd.DataFrame()
        self.json = {}
        STORAGE_FOLDER.mkdir(parents = True, exist_ok = True)

    def fetch_data(self):
        """
        Function to handle both downloading csv and generating json from multiple sources
        :return: Void
        """
        self._download_OWID_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
        self._download_GRT_csv('policy_facial_covering', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/h6m_facial_coverings.csv')
        self._download_GRT_csv('policy_school_closing', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c1m_school_closing.csv')
        self._download_GRT_csv('policy_public_transport', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c5m_close_public_transport.csv')
        self._download_GRT_csv('policy_gatherings_restriction', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c4m_restrictions_on_gatherings.csv')
        self._download_GRT_csv('policy_workplace_closing', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c2m_workplace_closing.csv')
        self._download_GRT_csv('policy_travel_restriction', 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/c8ev_internationaltravel.csv')
        
        self.interpolate('new_cases')
        
        self._save_csv()
        self._generate_json(FEATURES)

    def _download_OWID_csv(self, url: str):
        """
        Function to download and save csv file
        :return: Void
        """
        self.data = pd.read_csv(url)
        self.data = self.data.loc[self.data['iso_code'].isin(COUNTRIES)]

    def _download_GRT_csv(self, column: str, url: str):
        """
        Function to download the policy features from Government Response Tracker (https://www.bsg.ox.ac.uk/research/covid-19-government-response-tracker)
        :param: column: Column name to save the data to
        :param: url: URL to download the data from
        :return: Void
        """
        temporal_data = pd.read_csv(url)
        temporal_data = temporal_data.loc[temporal_data['country_code'].isin(COUNTRIES)]
        temporal_data = temporal_data.T
        temporal_data.columns = temporal_data.iloc[1]
        temporal_data = temporal_data[temporal_data.index.str.match('[0-9]+[a-zA-Z]+[0-9]+')]
        temporal_data = temporal_data.rename_axis(None, axis=1)
        temporal_data['date'] = temporal_data.index
        dates = []
        for date in temporal_data['date']:
            dates.append(parse(date))
        temporal_data['date'] = dates

        for index, row in self.data.iterrows():
            self.data.at[index, column] = temporal_data.loc[temporal_data['date'] == row['date']][row['iso_code']][0]

    def interpolate(self, feature: str):
        """
        Function to interpolate the data
        :return: Void
        """
        self.data[feature] = (self.data
        .assign(asset=self.data[feature].replace(0, float('nan')))
        .groupby('iso_code')[feature]
        .transform(lambda s: s[::-1].interpolate(limit=1).bfill())
        )

    def _save_csv(self):
        """
        Function to save the csv file
        :return: Void
        """

        self.data.to_csv(STORAGE_FOLDER / 'covid.csv', index=False)

    def _generate_json(self, category_dict: dict):
        """
        Function to generate json from csv file
        :param category_dict: Dictionary with categories as keys and features as values
        :return: Void
        """
        pd.set_option('display.max_rows', None, 'display.max_columns', None)

        print(self.data.isnull().sum())

        self.real_data = {}
        for category in category_dict:
            category_data = {}
            for country in self.data['iso_code'].unique():
                country_data = {}
                for _, row in self.data[self.data['iso_code'] == country].iterrows():
                    date_data = {}
                    for attribute in category_dict[category]:
                        if pd.isnull(row[attribute]):
                            date_data[attribute] = None
                        else:
                            date_data[attribute] = row[attribute]
                    country_data[row["date"]] = date_data
                category_data[country] = country_data
            self.real_data[category] = category_data
        self.json['data'] = self.real_data
        self.json['forecast'] = {}

        with open(STORAGE_FOLDER / 'covid.json', "w") as outfile:
            json.dump(self.json, outfile, allow_nan=True)


class StatusReporter:

    class Code(Enum):
        ERROR = 1
        SUCCESS = 2
        WARNING = 3

    @staticmethod
    def setup_file():
        if not Path.exists(STORAGE_FOLDER / 'status.json'):
            with open(STORAGE_FOLDER / 'status.json', mode='w', encoding='utf-8') as f:
                json.dump({'status_updates': []}, f)

    @staticmethod
    def report(title: str, message: str, code: Code):
        StatusReporter.setup_file()

        with open(STORAGE_FOLDER / 'status.json','r+') as file:
            file_data = json.load(file)
            file_data["status_updates"].append({'date': str(datetime.now()),'title': title, 'message': message, 'code': code.value})
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    

#StatusReporter.report("Model predictions could not be created", "Due to an error, no new model predictions could be made. Note that the shown data is not up-to-date and data and models are shown from 2022-11-13. Check dashboard later for new data.", StatusReporter.Code.SUCCESS)

#test = DataFetcher().fetch_data()


class Forecaster:
    def __init__(self):
        self.data = pd.read_csv(STORAGE_FOLDER / 'covid.csv')

    def forecast(self):
        regressors = {}
        regressors['RFR_new_cases_A'] = self._forecast_model()
        regressors['RFR_new_cases_B'] = self._forecast_model()

        cases = {'cases': regressors}

        with open(STORAGE_FOLDER / 'covid.json','r+') as file:
            file_data = json.load(file)
            file_data["forecast"] = cases
            file.seek(0)
            json.dump(file_data, file, indent = 4)

        print(cases)

    def _forecast_model(self, predicted_feature: str = 'new_cases'):
        steps = 5

        regressor = {}
        regressor['parameters'] = {
            'features': [], 
            'random_state': 123,
            'lags': 12
            }

        for country in self.data['iso_code'].unique():
            country_data = {}

            forecaster = ForecasterAutoreg(
                    regressor = RandomForestRegressor(random_state=123),
                    lags      = 12
                )

            lags_grid = [3, 10, [1, 5, 20, 50, 100, 150]]
            param_grid = {'n_estimators': [50, 100],
                        'max_depth': [5, 10, 15]}

            results_grid = grid_search_forecaster(
                                    forecaster  = forecaster,
                                    y           = self.data.loc[self.data['iso_code'] == country]['new_cases'],
                                    param_grid  = param_grid,
                                    lags_grid   = lags_grid,
                                    steps       = steps,
                                    refit       = True,
                                    metric      = 'mean_squared_error',
                                    initial_train_size = len(self.data.loc[self.data['iso_code'] == country]['new_cases']),
                                    return_best = True,
                                    verbose     = False
                        )

            print(results_grid)

            forecaster.fit(y = self.data.loc[self.data['iso_code'] == country]['new_cases'])
            
            predictions = forecaster.predict(steps=steps)
            predictions = predictions.to_frame()

            self.data['date'] = pd.to_datetime(self.data['date'])
            start_date = self.data.loc[self.data['iso_code'] == 'BRA']['date'].max()
            forecast_dates = pd.date_range(start_date+timedelta(days=1), start_date+timedelta(days=steps), freq='d')

            predictions.index = forecast_dates
            predictions['date'] = predictions.index

            for _, row in predictions.iterrows():
                date_data = {}
                date_data[predicted_feature] = row['pred']
                country_data[str(row["date"].date())] = date_data
        
            regressor[country] = country_data

        return regressor
        





test = Forecaster().forecast()
