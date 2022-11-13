from urllib.request import urlopen
import pandas as pd
import json
from pathlib import Path
from enum import Enum
from datetime import datetime
import requests
 
URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
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
    "policy": ["stringency_index"]
}

class Country(Enum):
    NORWAY = 1
    NETHERLANDS = 2
    SPAIN = 3
    BRAZIL = 4

class LiveDataFetcher:
    def __init__(self):
        self.data = {}
        STORAGE_FOLDER.mkdir(parents = True, exist_ok = True)

    def fetch_country(self, country: Country):
        if country == Country.NORWAY:
            return self.fetch_norway()
        elif country == Country.NETHERLANDS:
            return self.fetch_netherlands()
        elif country == Country.SPAIN:
            return self.fetch_spain()
        elif country == Country.BRAZIL:
            return self.fetch_brazil()
        else:
            raise ValueError("Country not supported")

    def fetch_norway(self):
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

    def fetch_netherlands(self):
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

    def fetch_spain(self):
        return self._fetch_covid_19_api("https://api.covid19api.com/dayone/country/spain")

    def fetch_brazil(self):
        return self._fetch_covid_19_api("https://api.covid19api.com/dayone/country/brazil")

    def _fetch_covid_19_api(self, url: str):
        response = requests.request("GET", url, headers={}, data={})
        result = json.loads(response.text)
        result = result[-2:]
        hours = (datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(result[0]['Date'], "%Y-%m-%dT%H:%M:%SZ")).days * 24
        date = str(datetime.strptime(result[1]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
        cases = result[1]['Confirmed'] - result[0]['Confirmed']
        deaths = result[1]['Deaths'] - result[0]['Deaths']

        return {'date': date, 'hours': hours, 'cases': cases, 'deaths': deaths}


test = LiveDataFetcher().fetch_country(Country.SPAIN)
print(test)


























class DataHandler:
    def __init__(self):
        self.data = pd.DataFrame()
        self.json = {}
        STORAGE_FOLDER.mkdir(parents = True, exist_ok = True)

    def fetch_data(self):
        self.data = pd.read_csv(URL)
        self.data = self.data.loc[self.data['iso_code'].isin(COUNTRIES)]
        self.data.to_csv(STORAGE_FOLDER / 'covid.csv', index=False)

    def generate_json(self, category_dict: dict):
        for category in category_dict:
            category_data = {}
            for country in self.data['iso_code'].unique():
                country_data = {}
                for _, row in self.data[self.data['iso_code'] == country].iterrows():
                    date_data = {}
                    for attribute in category_dict[category]:
                        date_data[attribute] = row[attribute]
                    country_data[row["date"]] = date_data
                category_data[country] = country_data
            self.json[category] = category_data

        with open(STORAGE_FOLDER / 'covid.json', "w") as outfile:
            json.dump(self.json, outfile)




# test = DataHandler()
# test.fetch_data()
# test.generate_json(FEATURES)




# def fetch_data():
#     cases_csv = pd.read_csv(URL)
#     cases_csv.to_csv('storage_mock/data/cases_world.csv', index=False) 
#     return cases_csv
#     # cases_csv = cases_csv.loc[cases_csv['iso_code'].isin(COUNTRIES)]
#     # cases_csv.to_csv('data/cases.csv', index=False) 

# def generate_json(dataframe: pd.DataFrame, features: dict):
#     meta_json = {}
#     for category in features:
#         category_data = {}
#         for country in dataframe['iso_code'].unique():
#             country_data = {}
#             for _, row in dataframe[dataframe['iso_code'] == country].iterrows():
#                 date_data = {}
#                 for attribute in features[category]:
#                     date_data[attribute] = row[attribute]
#                 country_data[row["date"]] = date_data
#             category_data[country] = country_data
#         meta_json[category] = category_data
#     return (meta_json)

# if __name__ == '__main__':
#     data = fetch_data()

#     with open("test.json", "w") as outfile:
#         json.dump(generate_json(fetch_data(), {"cases": ['new_cases', 'total_cases'], "deaths": ['new_deaths', 'total_deaths']}), outfile)
