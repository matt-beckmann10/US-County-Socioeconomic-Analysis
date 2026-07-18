import pandas as pd
from pathlib import Path
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# Set project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data_clean"

CLEAN_DIR.mkdir(exist_ok=True)


# Load files
df = pd.read_csv(CLEAN_DIR / "final_merged.csv")


# Average unemployment rate
df["avg_unemployment_rate"] = (
    df["2023_unemployment_rate"] +
    df["2024_unemployment_rate"]
) / 2

# Violent crime rates per 100,000
df["violent_rate_2023"] = (
    df["2023_violent_crime"] / df["population"]
) * 100000

df["violent_rate_2024"] = (
    df["2024_violent_crime"] / df["population"]
) * 100000

# Average violent crime rate
df["avg_violent_crime_rate"] = (
    df["violent_rate_2023"] +
    df["violent_rate_2024"]
) / 2

# Property crime rates per 100,000
df["property_rate_2023"] = (
    df["2023_property_crime"] / df["population"]
) * 100000

df["property_rate_2024"] = (
    df["2024_property_crime"] / df["population"]
) * 100000

# Average property crime rate
df["avg_property_crime_rate"] = (
    df["property_rate_2023"] +
    df["property_rate_2024"]
) / 2

# Metro status dummy variable
df["metro_dummy"] = (
    df["metro_status"] == "Metro"
).astype(int)


print(df[
    [
        "avg_unemployment_rate",
        "avg_violent_crime_rate",
        "avg_property_crime_rate",
        "metro_dummy"
    ]
].describe())


print(df[
    [
        "county",
        "population",
        "avg_violent_crime_rate",
        "avg_property_crime_rate",
        "metro_status",
        "metro_dummy"
    ]
].head())


df.to_csv(
    CLEAN_DIR / "analysis_ready.csv",
    index=False
)

# # Inspect final dataset
# print("\n-- Info --")
# print(df.info())
# print("\n-- Null Counts --")
# print(df.isnull().sum())
# print("\n-- Duplicates --")
# print(df.duplicated().sum())
# print("\n-- Describe --")
# print(df.describe())
# print("\n-- Head --")
# print(df.head())
# print("\n-- Tail --")
# print(df.tail())