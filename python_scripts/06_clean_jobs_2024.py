import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data_raw"
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load raw jobs file 2024
jobs_2024_clean = pd.read_excel(RAW_DIR / "laucnty24.xlsx", header=1)


# Rename columns
jobs_2024_clean = jobs_2024_clean.rename(columns={
    "State FIPS Code": "state_fips",
    "County FIPS Code": "county_fips",
    "County Name/State Abbreviation": "county_state",
    "Unemployment Rate (%)": "2024_unemployment_rate"
})


# Remove footer rows
jobs_2024_clean = jobs_2024_clean.dropna(
    subset=["state_fips"]
).copy()


# Create FIPS
jobs_2024_clean["state_fips"] = (
    jobs_2024_clean["state_fips"]
    .astype(float)
    .astype(int)
    .astype(str)
    .str.zfill(2)
)

jobs_2024_clean["county_fips"] = (
    jobs_2024_clean["county_fips"]
    .astype(float)
    .astype(int)
    .astype(str)
    .str.zfill(3)
)

jobs_2024_clean["fips_code"] = (
    jobs_2024_clean["state_fips"] + jobs_2024_clean["county_fips"]
)


# Split county and state
split = jobs_2024_clean["county_state"].str.split(
    ", ",
    n=1,
    expand=True
)

jobs_2024_clean["county"] = split[0]

jobs_2024_clean["state_abbrev"] = split[1]


# Keep needed columns only
jobs_2024_clean = jobs_2024_clean[
    [
        "fips_code",
        "2024_unemployment_rate"
    ]
]


# Save file
jobs_2024_clean.to_csv(
    CLEAN_DIR / "jobs_2024_clean.csv",
    index=False
)


print("--Info--")
print(jobs_2024_clean.info())
print("\n--Null Counts--")
print(jobs_2024_clean.isnull().sum())
print("\n--Duplicates--")
print(jobs_2024_clean.duplicated().sum())
print("\n--Describe--")
print(jobs_2024_clean.describe())
print("\n--Head--")
print(jobs_2024_clean.head())
print("\n--Tail--")
print(jobs_2024_clean.tail())