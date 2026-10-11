"""ETL pipeline for the Movies project.

Flow:
CSV + OMDb API -> Python/Pandas transformations -> SQLite

Credentials and local machine paths are intentionally excluded from this
public portfolio version. Configure them through environment variables.
"""

import os
import random
import sqlite3
from pathlib import Path

import pandas as pd
import requests


CSV_FILE_PATH = Path(os.getenv("MOVIES_CSV_PATH", "data/moviesc.csv"))
DB_PATH = Path(os.getenv("ETL_SQLITE_PATH", "data/movies_project.db"))
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
TABLE_NAME = "movies_cleaned"


def extract_csv(file_path: Path) -> pd.DataFrame:
    """Load and standardize the source CSV."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.upper()
        df.rename(
            columns={
                "MOVIES": "TITLE",
                "YEAR": "YEAR_CSV",
                "GENRE": "GENRE_CSV",
                "RATING": "RATING_CSV",
            },
            inplace=True,
        )
        df["SOURCE"] = "LocalCSV"
        print("CSV data loaded successfully.")
        return df
    except Exception as exc:
        print(f"Error reading CSV: {exc}")
        return pd.DataFrame()


def extract_random_api_data(title_list, n: int = 5) -> pd.DataFrame:
    """Fetch OMDb metadata for a random sample of movie titles."""
    if not OMDB_API_KEY:
        raise ValueError(
            "OMDB_API_KEY is not set. Add it as an environment variable before running."
        )

    sampled_titles = random.sample(title_list, min(n, len(title_list)))
    rows = []

    for title in sampled_titles:
        try:
            response = requests.get(
                "https://www.omdbapi.com/",
                params={"t": title, "apikey": OMDB_API_KEY},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "True":
                rows.append(
                    {
                        "TITLE": data.get("Title"),
                        "YEAR_API": data.get("Year"),
                        "GENRE_API": data.get("Genre"),
                        "RATING_API": data.get("imdbRating"),
                        "SOURCE": "OMDB_API",
                    }
                )
        except Exception as exc:
            print(f"API error for {title}: {exc}")

    return pd.DataFrame(rows)


def clean_and_merge(csv_df: pd.DataFrame, api_df: pd.DataFrame) -> pd.DataFrame:
    """Merge CSV and API data, handle missing values, and remove duplicates."""
    if csv_df.empty:
        print("CSV data is empty.")
        return pd.DataFrame()

    merged_df = pd.merge(
        csv_df,
        api_df,
        on="TITLE",
        how="left",
        suffixes=("_CSV", "_API"),
    )

    for col in ["YEAR_CSV", "GENRE_CSV"]:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].fillna("Unknown")

    for col in ["RATING_CSV", "RATING_API"]:
        if col in merged_df.columns:
            merged_df[col] = pd.to_numeric(
                merged_df[col], errors="coerce"
            ).fillna(0)
            merged_df[col] = merged_df[col].clip(lower=0)

    merged_df.drop_duplicates(subset=["TITLE"], inplace=True)

    print("Data cleaned and merged successfully.")
    return merged_df


def load_to_sqlite(df: pd.DataFrame, db_path: Path) -> None:
    """Load the cleaned dataset into SQLite."""
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        print("Data saved to SQLite.")
    except Exception as exc:
        print(f"Error saving to database: {exc}")


def main() -> None:
    print("Starting ETL process...")

    csv_df = extract_csv(CSV_FILE_PATH)
    if csv_df.empty or "TITLE" not in csv_df.columns:
        print("ETL failed: No valid CSV data to process.")
        return

    api_df = extract_random_api_data(
        csv_df["TITLE"].dropna().unique().tolist(),
        n=5,
    )

    print("API Data Preview:")
    print(api_df.head())

    cleaned_df = clean_and_merge(csv_df, api_df)

    if cleaned_df.empty:
        print("ETL failed: No data to process.")
        return

    output_csv = Path("data/cleaned_movies.csv")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to '{output_csv}'")

    load_to_sqlite(cleaned_df, DB_PATH)
    print("ETL process completed.")


if __name__ == "__main__":
    main()
