import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load files
acs_df = pd.read_csv(CLEAN_DIR / "acs_2023_clean.csv")
fbi_df = pd.read_csv(CLEAN_DIR / "fbi_merged.csv")


# Clean merge keys
for df in [acs_df, fbi_df]:
    df["state"] = df["state"].astype(str).str.strip()
    df["county"] = df["county"].astype(str).str.strip()


# Merge ACS and FBI
acs_fbi_merged = acs_df.merge(
    fbi_df,
    on=["state", "county"],
    how="left",
    indicator=True
)


# Check merge results
print("\n-- Merge Results --")
print(acs_fbi_merged["_merge"].value_counts())


# Save unmatched ACS rows for reference
acs_fbi_unmatched = acs_fbi_merged[
    acs_fbi_merged["_merge"] == "left_only"
].copy()

acs_fbi_unmatched.to_csv(
    CLEAN_DIR / "acs_fbi_unmatched.csv",
    index=False
)

print(f"\nSaved {len(acs_fbi_unmatched)} unmatched records to data_clean/acs_fbi_unmatched.csv")


# Keep only matched records
acs_fbi_merged = acs_fbi_merged[
    acs_fbi_merged["_merge"] == "both"
].copy()


# Drop merge indicator
acs_fbi_merged.drop(columns="_merge", inplace=True)

# Reorder column headers
acs_fbi_merged = acs_fbi_merged[
    [
        "fips_code",
        "state",
        "county",
        "population",
        "metro_status",
        "poverty_pct",
        "bachelors_pct",
        "median_income",
        "2023_violent_crime",
        "2024_violent_crime",
        "2023_property_crime",
        "2024_property_crime"
    ]
]


# Save final ACS and FBI merged file
acs_fbi_merged.to_csv(
    CLEAN_DIR / "acs_fbi_merged.csv",
    index=False
)


# Inspect final merged dataset
print("\n-- Info --")
print(acs_fbi_merged.info())
print("\n-- Null Counts --")
print(acs_fbi_merged.isnull().sum())
print("\n-- Duplicates --")
print(acs_fbi_merged.duplicated().sum())
print("\n-- Describe --")
print(acs_fbi_merged.describe())
print("\n-- Head --")
print(acs_fbi_merged.head())
print("\n-- Tail --")
print(acs_fbi_merged.tail())
