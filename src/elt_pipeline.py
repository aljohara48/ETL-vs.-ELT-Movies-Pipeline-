"""ELT pipeline for the Movies project.

Recovered implementation scope:
SQLite + CSV -> Great Expectations validation -> PostgreSQL staging tables

The SQL transformation stage was performed separately in PostgreSQL/pgAdmin
in the original project and is not included here because the original SQL
script was not among the recovered source files.

Credentials and local machine paths are intentionally excluded from this
public portfolio version.
"""

import os
import sqlite3
import time
from pathlib import Path

import great_expectations as ge
import pandas as pd
from sqlalchemy import create_engine


SQLITE_SOURCE_PATH = Path(os.getenv("ELT_SQLITE_SOURCE", "data/movies.db"))
CSV_SOURCE_PATH = Path(os.getenv("ELT_CSV_SOURCE", "data/sampled_cleaned.csv"))
POSTGRES_URL = os.getenv("POSTGRES_URL")


def extract_data():
    """Extract raw movie data from SQLite and CSV sources."""
    with sqlite3.connect(SQLITE_SOURCE_PATH) as sqlite_conn:
        df_movie_showtimes = pd.read_sql_query(
            "SELECT * FROM movies",
            sqlite_conn,
        )

    df_movies = pd.read_csv(CSV_SOURCE_PATH)
    return df_movie_showtimes, df_movies


def validate_data(df_movie_showtimes, df_movies):
    """Apply the original project validation rules using Great Expectations."""
    ge_movie_showtimes = ge.from_pandas(df_movie_showtimes)
    ge_movies = ge.from_pandas(df_movies)

    ge_movie_showtimes.expect_column_values_to_not_be_null("ID")
    ge_movies.expect_column_values_to_be_between(
        "RATING",
        min_value=0,
        max_value=10,
    )

    movie_showtimes_result = ge_movie_showtimes.validate()
    movies_result = ge_movies.validate()

    print("MovieShowtimes Validation:")
    print(movie_showtimes_result)

    print("\nMovies Validation:")
    print(movies_result)

    return (
        bool(movie_showtimes_result["success"]),
        bool(movies_result["success"]),
    )


def load_to_postgres(df_movie_showtimes, df_movies):
    """Load validated raw data into PostgreSQL staging tables."""
    if not POSTGRES_URL:
        raise ValueError(
            "POSTGRES_URL is not set. Add it as an environment variable before running."
        )

    engine = create_engine(POSTGRES_URL)

    df_movie_showtimes.to_sql(
        "stage_MovieShowtimes",
        engine,
        if_exists="replace",
        index=False,
    )
    df_movies.to_sql(
        "stage_movies",
        engine,
        if_exists="replace",
        index=False,
    )

    print("Data successfully loaded into PostgreSQL staging tables.")


def main():
    start_time = time.time()

    df_movie_showtimes, df_movies = extract_data()
    valid_movie_showtimes, valid_movies = validate_data(
        df_movie_showtimes,
        df_movies,
    )

    if valid_movie_showtimes and valid_movies:
        load_to_postgres(df_movie_showtimes, df_movies)
    else:
        print("Data validation failed. Data not loaded to PostgreSQL.")

    run_time_seconds = time.time() - start_time
    print(f"Run time: {run_time_seconds:.4f} seconds")


if __name__ == "__main__":
    main()
