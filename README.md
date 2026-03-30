# US Hospital Cost & Quality Analytics Platform

A data engineering and analytics project built on publicly available CMS data. Transforms raw hospital datasets into a structured analytics layer for evaluating cost efficiency, quality of care, and patient experience across US hospitals.

---

## Objectives

- Which hospitals are most cost-efficient?
- Where are readmission and mortality rates highest?
- How does patient satisfaction relate to cost and outcomes?
- Which hospitals deliver the best overall value?

---

## Architecture

```
Raw CSV Data → Python ETL → PostgreSQL Staging → dbt Models → Analytics Warehouse → Dashboard
```

---

## Tech Stack

**Data Engineering**

- Python (Pandas)
- PostgreSQL
- dbt
- Docker _(optional)_
- Airflow _(optional)_

**Analytics & Visualization**

- Tableau / Power BI / Metabase

---

## Data Sources

All datasets are publicly available from the Centers for Medicare & Medicaid Services (CMS):

| Dataset                                  | Description                          |
| ---------------------------------------- | ------------------------------------ |
| Hospital General Information             | Facility identifiers, type, location |
| Hospital Readmissions Reduction Program  | Readmission rates by measure         |
| Patient Survey (HCAHPS)                  | Patient satisfaction scores          |
| Medicare Spending Per Beneficiary (MSPB) | Cost per episode of care             |

---

## Data Model

**Fact Table**

`fact_hospital_performance` — hospital_id, measure_id, cost, readmission_rate, mortality_rate, patient_rating, year

**Dimension Tables**

`dim_hospital` — hospital_id, hospital_name, state, city, hospital_type

`dim_measure` — measure_id, measure_name, measure_category

`dim_date` — date_key, year, quarter

---

## Analytical Focus Areas

**Cost Efficiency** — Cost distribution by hospital and region, identification of high-cost providers, cost trends over time

**Quality of Care** — Readmission rate analysis, mortality rate comparison, identification of high-risk hospitals

**Patient Experience** — Satisfaction analysis, relationship between satisfaction and outcomes, regional variation in ratings

**Cost vs. Quality** — Identification of high-value hospitals, detection of inefficient providers, tradeoff analysis between cost and outcomes

**Geographic Analysis** — State-level performance comparisons, regional disparities in care

**Hospital Type Analysis** — Performance by hospital type, ownership and structural comparisons

---

## Project Workflow

**1. Data Collection**
Acquire CMS datasets in CSV format and store raw files in a structured directory.

**2. Data Cleaning (Python)**
Standardize column names, handle missing values, convert data types, remove duplicates.

**3. Data Loading**
Load cleaned data into PostgreSQL staging tables and validate schema and row counts.

**4. Data Modeling**
Build fact and dimension tables using a star schema via SQL and dbt.

**5. Analysis**
Develop analytical queries and create derived metrics and KPIs.

**6. Visualization**
Build dashboards with filtering by hospital, region, and measure.

---

## Project Status

Active development. See `project_notes.md` for a running log of data decisions, problems encountered, and solutions applied.
