# 🎬 Movie ETL vs ELT Data Pipeline

A data engineering project that builds and compares **ETL** and **ELT**
pipelines using a movie dataset.

The project demonstrates data extraction, validation, transformation,
storage, automation, and visualization using modern data engineering tools.

---

## 🔄 ETL Pipeline

**CSV + OMDb API → Python Transformation → SQLite → Power BI**

The ETL pipeline:

- Extracted movie data from CSV and the OMDb API
- Cleaned and standardized the data using Python and Pandas
- Handled missing values and duplicates
- Merged external movie metadata
- Loaded the final dataset into SQLite
- Visualized the processed data using Power BI

---

## ⚙️ ELT Pipeline

**CSV + SQLite → Validation → PostgreSQL → SQL Transformation**

The ELT pipeline:

- Extracted raw data from CSV and SQLite
- Validated data using Great Expectations
- Loaded raw data into PostgreSQL staging tables
- Applied SQL transformations inside PostgreSQL
- Cleaned null values, duplicates, text fields, years, and ratings
- Produced analysis-ready final tables

---

## 🛠️ Technologies

- Python
- Pandas
- SQL
- SQLite
- PostgreSQL
- SQLAlchemy
- Great Expectations
- OMDb API
- Power BI
- Windows Task Scheduler

---

## ✅ Data Quality

Validation rules included:

- Required ID values must not be null
- Movie ratings must be between 0 and 10
- Duplicate removal
- Missing-value handling
- Data type validation
- Text standardization

---

## 📊 ETL vs ELT

| Metric | ETL | ELT |
|---|---|---|
| Execution Time | 6 sec | 0.5643 sec |
| Scalability | Lower | Higher |
| Efficiency | Lower | Higher |

In this project's test environment, the ELT pipeline completed faster
and provided greater flexibility by performing transformations directly
inside PostgreSQL.

---

## 📈 Dashboard

The final cleaned movie data was visualized using **Power BI** to explore
movie ratings, genres, release years, and summary metrics.

---

Academic team project – Princess Nourah bint Abdulrahman University
