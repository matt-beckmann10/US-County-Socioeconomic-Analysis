import pandas as pd
from pathlib import Path


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load clean FBI files
fbi_2023_clean = pd.read_csv(CLEAN_DIR / "fbi_2023_clean.csv")
fbi_2024_clean = pd.read_csv(CLEAN_DIR / "fbi_2024_clean.csv")


# Remove law-enforcement agency rows, if any slipped through
agency_pattern = "police|sheriff"

fbi_2023_clean = fbi_2023_clean[
    ~fbi_2023_clean["county"].str.contains(agency_pattern, case=False, na=False)
].copy()

fbi_2024_clean = fbi_2024_clean[
    ~fbi_2024_clean["county"].str.contains(agency_pattern, case=False, na=False)
].copy()


# Clean merge keys
for df in [fbi_2023_clean, fbi_2024_clean]:
    df["state"] = df["state"].astype(str).str.strip()
    df["county"] = df["county"].astype(str).str.strip()


# Check for duplicate merge keys before merging
print("\n-- 2023 duplicate state/county keys --")
print(fbi_2023_clean[fbi_2023_clean.duplicated(["state", "county"], keep=False)])

print("\n-- 2024 duplicate state/county keys --")
print(fbi_2024_clean[fbi_2024_clean.duplicated(["state", "county"], keep=False)])


# Optional: compare weird county names before merge
f23_weird = fbi_2023_clean[
    fbi_2023_clean["county"].str.contains(r"[^\w\s]", regex=True, na=False)
][["state", "county"]]

f24_weird = fbi_2024_clean[
    fbi_2024_clean["county"].str.contains(r"[^\w\s]", regex=True, na=False)
][["state", "county"]]

comparison = f23_weird.merge(
    f24_weird,
    on=["state", "county"],
    how="outer",
    indicator=True
)

print("\n-- Weird county name comparison --")
print(comparison)


# Merge 2023 and 2024 side-by-side
fbi_merged = fbi_2023_clean.merge(
    fbi_2024_clean,
    on=["state", "county"],
    how="left",
    indicator=True
)


# Check unmatched 2023 counties
unmatched = fbi_merged[fbi_merged["_merge"] != "both"]

print("\n-- 2023 counties not matched to 2024 --")
print(unmatched[["state", "county", "_merge"]])


# Drop merge indicator after checking
fbi_merged = fbi_merged.drop(columns=["_merge"])


# Drop rows missing 2024 data
# This keeps only counties that exist in both 2023 and 2024.
fbi_merged = fbi_merged.dropna()


metro_compare = fbi_merged[
    fbi_merged['2023_metro_status'] != fbi_merged['2024_metro_status']
]

print(metro_compare[
    ['state',
     'county',
     '2023_metro_status',
     '2024_metro_status',]
    ])

# Mineral County, Montana changed metro status in mid-2023. -
# Reduce to one column for metro status
fbi_merged["metro_status"] = fbi_merged["2024_metro_status"]

# Remove the old columns
fbi_merged.drop(
    columns=["2024_metro_status",
             "2023_metro_status"
    ],
    inplace=True
)


# Save merged FBI file
output_path = CLEAN_DIR / "fbi_merged.csv"

fbi_merged.to_csv(output_path, index=False)


# Inspect final merged data
print("\n-- Info --")
print(fbi_merged.info())
print("\n-- Null Counts --")
print(fbi_merged.isnull().sum())
print("\n-- Duplicates --")
print(fbi_merged.duplicated().sum())
print("\n-- Describe --")
print(fbi_merged.describe())
print("\n-- Head --")
print(fbi_merged.head())
print("\n-- Tail --")
print(fbi_merged.tail())
