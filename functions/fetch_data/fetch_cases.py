from urllib.request import urlopen
import pandas as pd

URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
COUNTRIES = ["NLD", "BRA", "NOR", "ESP"]

cases_json = pd.read_csv(URL)
cases_json.to_csv('data/cases_world.csv', index=False) 

cases_json = cases_json.loc[cases_json['iso_code'].isin(COUNTRIES)]
cases_json.to_csv('data/cases.csv', index=False) 

