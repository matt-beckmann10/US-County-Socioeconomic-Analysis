import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load cleaned jobs files
jobs_2023 = pd.read_csv(CLEAN_DIR / "jobs_2023_clean.csv")
jobs_2024 = pd.read_csv(CLEAN_DIR / "jobs_2024_clean.csv")


# Clean merge keys
for df in [jobs_2023, jobs_2024]:
    df["fips_code"] = df["fips_code"].astype(str).str.zfill(5)


# Check for duplicate merge keys
print("\n-- 2023 duplicate FIPS keys --")
print(jobs_2023[jobs_2023.duplicated("fips_code", keep=False)])

print("\n-- 2024 duplicate FIPS keys --")
print(jobs_2024[jobs_2024.duplicated("fips_code", keep=False)])


# Merge
jobs_merged = jobs_2023.merge(
    jobs_2024,
    on="fips_code",
    how="inner",
    indicator=True
)


# Check unmatched
print("\n-- Merge Results --")
print(jobs_merged["_merge"].value_counts())


# Remove merge indicator
jobs_merged.drop(columns="_merge", inplace=True)


# Save
output_path = CLEAN_DIR / "jobs_merged.csv"

jobs_merged.to_csv(
    output_path,
    index=False
)


# Inspect
print("\n-- Info --")
print(jobs_merged.info())
print("\n-- Null Counts --")
print(jobs_merged.isnull().sum())
print("\n-- Duplicates --")
print(jobs_merged.duplicated().sum())
print("\n-- Describe --")
print(jobs_merged.describe())
print("\n-- Head --")
print(jobs_merged.head())
print("\n-- Tail --")
print(jobs_merged.tail())