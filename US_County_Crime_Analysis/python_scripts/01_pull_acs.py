import pandas as pd
import requests
from pathlib import Path


# API script to pull American Community Survey 2023 data

# Settings
CENSUS_KEY = "162b68a889eb7f7778f32f284de5facac1a49a80"
YEAR = 2023

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data_raw"

RAW_DIR.mkdir(exist_ok=True)


# Pull ACS subject data
subject_variables = [
    "S1701_C03_001E",  # Poverty %
    "S1501_C02_015E",  # % Bachelor's degree or higher, age 25+
    "S1901_C01_012E",  # Median household income
]

subject_url = f"https://api.census.gov/data/{YEAR}/acs/acs5/subject"

subject_params = {
    "get": ",".join(["NAME"] + subject_variables),
    "for": "county:*",
    "in": "state:*",
    "key": CENSUS_KEY,
}

subject_response = requests.get(subject_url, params=subject_params)
subject_response.raise_for_status()

subject_data = subject_response.json()

acs_subject_raw = pd.DataFrame(
    subject_data[1:],
    columns=subject_data[0]
)

acs_subject_raw.to_csv(
    RAW_DIR / f"acs_subject_{YEAR}_raw.csv",
    index=False
)

print(f"Saved ACS subject data to data_raw/acs_subject_{YEAR}_raw.csv")


# Pull ACS population data
population_variables = [
    "B01003_001E"  # Total population
]

population_url = f"https://api.census.gov/data/{YEAR}/acs/acs5"

population_params = {
    "get": ",".join(["NAME"] + population_variables),
    "for": "county:*",
    "in": "state:*",
    "key": CENSUS_KEY,
}

population_response = requests.get(population_url, params=population_params)
population_response.raise_for_status()

population_data = population_response.json()

acs_population_raw = pd.DataFrame(
    population_data[1:],
    columns=population_data[0]
)

acs_population_raw.to_csv(
    RAW_DIR / f"acs_population_{YEAR}_raw.csv",
    index=False
)

print(f"Saved ACS population data to data_raw/acs_population_{YEAR}_raw.csv")
