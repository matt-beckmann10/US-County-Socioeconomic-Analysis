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
fbi_2023_raw = pd.read_excel(RAW_DIR / "fbi_2023_data.xlsx",header=4)

fbi_2023_clean = fbi_2023_raw.copy()


# Clean fbi_2023

# Ensure State has real NaN (not the string "nan")
fbi_2023_clean['State'] = fbi_2023_clean['State'].replace(['nan', 'NaN', 'None', ''], None)

# Use a helper series for pattern matching
state_text = fbi_2023_clean['State'].fillna('')

# Detect the "header" rows that contain metro/nonmetro labels
is_metro_hdr = state_text.str.contains(r'-\s*Metropolitan Counties', case=False, na=False)
is_nonmetro_hdr = state_text.str.contains(r'-\s*Nonmetropolitan Counties', case=False, na=False)

# Create metro_status column and add those "header" rows to it
fbi_2023_clean['metro_status'] = np.select(
    [is_metro_hdr, is_nonmetro_hdr],
    ['Metro', 'Non-Metro'],
    default=None
)

# Convert string "nan"/"NaN"/"" to real missing values
fbi_2023_clean['metro_status'] = (
    fbi_2023_clean['metro_status'].replace(['nan', 'NaN', 'None', ''], np.nan)
)

# Use forward fill to fill in each row's metro_status value
fbi_2023_clean['metro_status'] = fbi_2023_clean['metro_status'].ffill()


# Now remove junk from 'State' column
state_text = fbi_2023_clean['State'].fillna('')

# Identify header rows
is_header = state_text.str.contains('-', na=False)

# Extract state name (text before the dash)
fbi_2023_clean['state_clean'] = np.where(
    is_header,
    state_text.str.split('-').str[0].str.strip(),
    np.nan
)

# Use forward fill to assign state names to each row
fbi_2023_clean['state_clean'] = fbi_2023_clean['state_clean'].ffill()

# Replace original 'State' column with 'state_clean'
fbi_2023_clean['State'] = fbi_2023_clean['state_clean']
fbi_2023_clean = fbi_2023_clean.drop(columns=['state_clean'])

# Replace all caps on state names
fbi_2023_clean['State'] = fbi_2023_clean['State'].str.strip().str.title()


# Drop unnecessary columns
fbi_2023_clean.drop(columns=['Murder and\nnonnegligent\nmanslaughter',
                           'Rape',
                           'Robbery',
                           'Aggravated\nassault',
                           'Burglary',
                           'Larceny-\ntheft',
                           'Motor\nvehicle\ntheft',
                           'Arson1'
                          ], inplace=True)


# Standardize column headers
fbi_2023_clean = fbi_2023_clean.rename(columns={
    'Violent\ncrime' : 'violent_crime',
    'Property\ncrime' : 'property_crime'
})

fbi_2023_clean.columns = fbi_2023_clean.columns.str.lower()


# Drop nulls
fbi_2023_clean = fbi_2023_clean.dropna(subset=['violent_crime', 'property_crime'])


# Fix Florida typo
fbi_2023_clean['state'] = fbi_2023_clean['state'].replace('Florida2', 'Florida')


# Rename crime headers to reflect year
fbi_2023_clean = fbi_2023_clean.rename(columns={
    'violent_crime' : '2023_violent_crime',
    'property_crime' : '2023_property_crime',
    'metro_status' : '2023_metro_status'
})

# Create fbi_2023_clean.csv
fbi_2023_clean.to_csv(
    CLEAN_DIR / "fbi_2023_clean.csv",
    index=False
)


print("--Info--")
print(fbi_2023_clean.info())
print("\n--Null Counts--")
print(fbi_2023_clean.isnull().sum())
print("\n--Duplicates--")
print(fbi_2023_clean.duplicated().sum())
print("\n--Describe--")
print(fbi_2023_clean.describe())
print("\n--Head--")
print(fbi_2023_clean.head())
print("\n--Tail--")
print(fbi_2023_clean.tail())