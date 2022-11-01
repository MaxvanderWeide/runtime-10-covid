from urllib.request import urlopen
import pandas as pd
import json

URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
COUNTRIES = ["NLD", "BRA", "NOR", "ESP"]

def fetch_data():
    cases_csv = pd.read_csv(URL)
    cases_csv.to_csv('storage_mock/data/cases_world.csv', index=False) 
    return cases_csv
    # cases_csv = cases_csv.loc[cases_csv['iso_code'].isin(COUNTRIES)]
    # cases_csv.to_csv('data/cases.csv', index=False) 

def generate_json(dataframe: pd.DataFrame, features: dict):
    meta_json = {}
    for category in features:
        category_data = {}
        for country in dataframe['iso_code'].unique():
            country_data = {}
            for _, row in dataframe[dataframe['iso_code'] == country].iterrows():
                date_data = {}
                for attribute in features[category]:
                    date_data[attribute] = row[attribute]
                country_data[row["date"]] = date_data
            category_data[country] = country_data
        meta_json[category] = category_data
    return (meta_json)

if __name__ == '__main__':
    with open("test.json", "w") as outfile:
        json.dump(generate_json(fetch_data(), {"cases": ['new_cases', 'total_cases'], "deaths": ['new_deaths', 'total_deaths']}), outfile)
