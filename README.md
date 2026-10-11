# 🎬 ETL vs. ELT Movies Pipeline

A data engineering project comparing **ETL** and **ELT** pipelines using a movie dataset.

The project demonstrates data extraction, validation, transformation, storage,
automation, and visualization.

---

## 🔄 ETL Pipeline

**CSV + OMDb API → Python/Pandas → SQLite → Power BI**

- Extracted movie data from CSV and the OMDb API
- Cleaned and standardized data using Python and Pandas
- Handled missing values and duplicates
- Merged external movie metadata
- Loaded the transformed data into SQLite
- Visualized the final data using Power BI

---

## ⚙️ ELT Pipeline

**CSV + SQLite → Great Expectations → PostgreSQL → SQL Transformation**

- Extracted raw data from CSV and SQLite
- Validated data using Great Expectations
- Loaded validated data into PostgreSQL staging tables
- Applied SQL-based transformations in PostgreSQL
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

Validation included:

- Non-null ID checks
- Rating range validation (0–10)
- Duplicate removal
- Missing-value handling
- Data type validation
- Text standardization

---

## 📊 ETL vs. ELT

| Metric | ETL | ELT |
|---|---:|---:|
| Execution Time | 6 sec | 0.5643 sec |
| Scalability | Lower | Higher |
| Efficiency | Lower | Higher |

In this project's test environment, the ELT pipeline completed faster
by performing transformations directly inside PostgreSQL.

---

## 💻 Source Code

- [ETL Pipeline](src/etl_pipeline.py)
- [ELT Pipeline](src/elt_pipeline.py)

---

## 📈 Dashboard

The final movie data was visualized using **Power BI** to explore ratings,
genres, release years, and summary metrics.

![Power BI Dashboard](Images/powerbi_dashboard.png)

---

Academic team project – Princess Nourah bint Abdulrahman University
