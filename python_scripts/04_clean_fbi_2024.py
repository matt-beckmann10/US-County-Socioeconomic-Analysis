import pandas as pd
import numpy as np
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data_raw"
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load raw FBI files
fbi_2024_raw = pd.read_excel(RAW_DIR / "fbi_2024_data.xlsx", header=4)

fbi_2024_clean = fbi_2024_raw.copy()


# Clean fbi_2024_clean table
# Drop last two rows (junk)
fbi_2024_clean = fbi_2024_clean.drop(index=[2444, 2445]).reset_index(drop=True)


# Drop unnecessary columns
fbi_2024_clean.drop(columns=['Murder and\nnonnegligent\nmanslaughter',
                           'Rape',
                           'Robbery',
                           'Aggravated\nassault',
                           'Burglary',
                           'Larceny-\ntheft',
                           'Motor\nvehicle\ntheft',
                           'Arson1'
                          ], inplace=True)


# Standardize column headers
fbi_2024_clean = fbi_2024_clean.rename(columns={
    'Metropolitan/Nonmetropolitan' : 'metro_status',
    'Violent\ncrime' : 'violent_crime',
    'Property\ncrime' : 'property_crime'
})

# Set headers to lowercase
fbi_2024_clean.columns = fbi_2024_clean.columns.str.lower()

# Replace all caps on state names
fbi_2024_clean['state'] = fbi_2024_clean['state'].str.strip().str.title()

# Fix Florida typo
fbi_2024_clean['state'] = fbi_2024_clean['state'].replace('Florida2', 'Florida')


# Standardize metro_status in 2024 dataset
fbi_2024_clean['metro_status'] = fbi_2024_clean['metro_status'].replace({
    'Metropolitan County': 'Metro',
    'Nonmetropolitan County': 'Non-Metro'
})

# Correct Iowa duplicate -
# (second 'Adams County' value supposed to be 'Carroll')
fbi_2024_clean.loc[578, 'county'] = 'Carroll'


# Rename crime headers to reflect year
fbi_2024_clean = fbi_2024_clean.rename(columns={
    'violent_crime' : '2024_violent_crime',
    'property_crime' : '2024_property_crime',
    'metro_status' : '2024_metro_status' # For post-merge verification
})



# Create fbi_2024_clean.csv
fbi_2024_clean.to_csv(
    CLEAN_DIR / "fbi_2024_clean.csv",
    index=False
)


print("--Info--")
print(fbi_2024_clean.info())
print("\n--Null Counts--")
print(fbi_2024_clean.isnull().sum())
print("\n--Duplicates--")
print(fbi_2024_clean.duplicated().sum())
print("\n--Describe--")
print(fbi_2024_clean.describe())
print("\n--Head--")
print(fbi_2024_clean.head())
print("\n--Tail--")
print(fbi_2024_clean.tail())