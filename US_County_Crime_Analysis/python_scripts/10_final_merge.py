import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load files
acs_fbi_df = pd.read_csv(CLEAN_DIR / "acs_fbi_merged.csv")
jobs_df = pd.read_csv(CLEAN_DIR / "jobs_merged.csv")


# Clean merge keys
for df in [acs_fbi_df, jobs_df]:
    df["fips_code"] = df["fips_code"].astype(str).str.zfill(5)


# Check duplicate FIPS keys before merging
print("\n-- ACS/FBI duplicate FIPS keys --")
print(acs_fbi_df[acs_fbi_df.duplicated("fips_code", keep=False)])

print("\n-- Jobs duplicate FIPS keys --")
print(jobs_df[jobs_df.duplicated("fips_code", keep=False)])


# Merge ACS/FBI with jobs data
final_df = acs_fbi_df.merge(
    jobs_df,
    on="fips_code",
    how="outer",
    indicator=True
)


# Check merge results
print("\n-- Merge Results --")
print(final_df["_merge"].value_counts())


# Save unmatched ACS/FBI rows for reference
final_unmatched_jobs = final_df[
    final_df["_merge"] == "right_only"
].copy()

final_unmatched_jobs.to_csv(
    CLEAN_DIR / "final_unmatched_jobs.csv",
    index=False
)

print(f"\nSaved {len(final_unmatched_jobs)} unmatched records to data_clean/final_unmatched_jobs.csv")


# Keep only matched records
final_df = final_df[
    final_df["_merge"] == "both"
].copy()

# Drop merge indicator
final_df.drop(columns="_merge", inplace=True)


# Reorder columns
final_df = final_df[
    [
        "fips_code",
        "state",
        "county",
        "population",
        "metro_status",
        "poverty_pct",
        "bachelors_pct",
        "median_income",
        "2023_unemployment_rate",
        "2024_unemployment_rate",
        "2023_violent_crime",
        "2024_violent_crime",
        "2023_property_crime",
        "2024_property_crime"
    ]
]


# Save final merged file
output_path = CLEAN_DIR / "final_merged.csv"

final_df.to_csv(output_path, index=False)


# Inspect final dataset
print("\n-- Info --")
print(final_df.info())
print("\n-- Null Counts --")
print(final_df.isnull().sum())
print("\n-- Duplicates --")
print(final_df.duplicated().sum())
print("\n-- Describe --")
print(final_df.describe())
print("\n-- Head --")
print(final_df.head())
print("\n-- Tail --")
print(final_df.tail())