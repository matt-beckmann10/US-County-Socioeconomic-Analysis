import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data_raw"
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load raw ACS files
acs_subject = pd.read_csv(RAW_DIR / "acs_subject_2023_raw.csv")
acs_population = pd.read_csv(RAW_DIR / "acs_population_2023_raw.csv")


# Rename columns
acs_subject = acs_subject.rename(columns={
    "S1701_C03_001E": "poverty_pct",
    "S1501_C02_015E": "bachelors_pct",
    "S1901_C01_012E": "median_income",

})

acs_population = acs_population.rename(columns={
    "B01003_001E": "population"
})


# Create FIPS codes
acs_subject["state"] = acs_subject["state"].astype(str).str.zfill(2)
acs_subject["county"] = acs_subject["county"].astype(str).str.zfill(3)
acs_subject["fips_code"] = acs_subject["state"] + acs_subject["county"]

acs_population["state"] = acs_population["state"].astype(str).str.zfill(2)
acs_population["county"] = acs_population["county"].astype(str).str.zfill(3)
acs_population["fips_code"] = acs_population["state"] + acs_population["county"]


# Convert numeric columns
subject_cols = [
    "poverty_pct",
    "bachelors_pct",
    "median_income"
]

for col in subject_cols:
    acs_subject[col] = pd.to_numeric(acs_subject[col], errors="coerce")

acs_population["population"] = pd.to_numeric(
    acs_population["population"],
    errors="coerce"
)


# Merge ACS subject + population data
acs_clean = acs_subject.merge(
    acs_population[["fips_code", "population"]],
    on="fips_code",
    how="left"
)


# Reorder columns
acs_clean = acs_clean[
    [
        "fips_code",
        "state",
        "county",
        "NAME",
        "population",
        "poverty_pct",
        "bachelors_pct",
        "median_income"
    ]
]


# Remove negative values from median_income
acs_clean = acs_clean.query("median_income >= 0")

# Clean up NAME column
# First, split NAME into two parts
name_split = acs_clean['NAME'].str.split(',', n=1, expand=True)

name_county = name_split[0]
name_state = name_split[1]

# Replace values in 'state' and 'county' with the split values from 'NAME'
acs_clean['county'] = name_county
acs_clean['state'] = name_state

# Drop 'NAME' and rearrange table columns
acs_clean = acs_clean[['fips_code',
                       'state',
                       'county',
                       'population',
                       'poverty_pct',
                       'bachelors_pct',
                       'median_income'
                       ]]


# Search for suffix words like 'county' or 'city' to remove
suffix_words = (name_county.str.split().str[-1].value_counts())


# Create list of words for removal
suffix_list = suffix_words.index.tolist()

# List modification
remove_words = ['Area', 'Region', 'Columbia']
suffix_list = [word for word in suffix_list if word not in remove_words]

suffix_list.extend(['City and Borough', 'Census Area', 'Planning Region'])


# Reorder the list to prevent errors
suffix_list = [
    'City and Borough',
    'Planning Region',
    'Census Area',
    'County',
    'Municipio',
    'Parish',
    'city',
    'Borough',
    'Municipality',
    'Columbia',
    'City'
    ]


# Remove all the words in the suffix_list from 'county'
# only if they occur at the end of the county name
for word in suffix_list:
    mask = acs_clean['county'].str.lower().str.endswith(' ' + word.lower())

    acs_clean.loc[mask, 'county'] = (
        acs_clean.loc[mask, 'county']
        .str.slice(0, -len(word) - 1)
        .str.strip()
    )


# Save cleaned ACS file
output_path = CLEAN_DIR / "acs_2023_clean.csv"

acs_clean.to_csv(output_path, index=False)

print(f"Saved cleaned ACS data to: {output_path}")
print(acs_clean.head())


# Examine acs_clean table
print("--Info--")
print(acs_clean.info())
print("\n--Null Counts--")
print(acs_clean.isnull().sum())
print("\n--Duplicates--")
print(acs_clean.duplicated().sum())
print("\n--Describe--")
print(acs_clean.describe())
print("\n--Head--")
acs_clean.head()

