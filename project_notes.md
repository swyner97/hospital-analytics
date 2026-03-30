# Project Notes — Hospital Analytics (CMS Data)

## Project Overview

**Goal:** Build a clean, analysis-ready dataset from CMS hospital data to evaluate hospital performance across readmissions, quality, and outcomes.

**Data Source:** CMS (Centers for Medicare & Medicaid Services)

**Tools:** Python, Pandas, Jupyter Notebook, SQL (planned), Tableau/Power BI (planned)

---

## Decision Log

### 1. Column Selection

**Observation:** The raw dataset contained many columns unrelated to readmission analysis.

**Problem:** Excess columns introduce noise and reduce clarity.

**Decision:** Retained only columns relevant to readmission performance — facility identifiers, measure counts, and comparative outcome indicators (Better / No Different / Worse).

---

### 2. Data Type Standardization

**Observation:** Columns were not consistently typed after import.

**Problem:** Incorrect types cause errors during aggregation and unreliable numeric operations.

**Decision:** Converted facility ID to integer, facility name to string, and all count columns to nullable integers. Nullable integers were used specifically to handle missing values safely, which standard integers do not support.

---

### 3. Aggregation to Hospital Level

**Observation:** The dataset contained multiple rows per hospital rather than one row per facility.

**Problem:** Multi-row structure makes analysis inconsistent, joins unreliable, and metrics prone to duplication.

**Decision:** Grouped by Facility ID to reduce the dataset to one row per hospital.

**Solution breakdown:**
- Count columns (Better, Worse, No Different, total measures) were summed — these represent cumulative values that accumulate across rows.
- The measure group count column was aggregated with max — this value is repeated identically across rows for each hospital, so summing it would inflate the result.
- Facility name was taken as first — the value is consistent across rows and requires no further logic.

---

### 4. Duplicate Validation

**Observation:** After aggregation, the dataset needed to be verified before use in any joins or further analysis.

**Problem:** An incorrect aggregation would silently produce duplicate hospital records, corrupting downstream analysis.

**Decision:** Ran a duplicate check on Facility ID after aggregation. Result was zero duplicates, confirming the dataset is hospital-level and safe for merging.

---

## Next Steps

- Merge with additional CMS datasets (mortality, patient experience)
- Create derived metrics: percentage of measures rated Better vs. Worse, overall performance score
- Statistical analysis: correlation and regression
- Build dashboard in Tableau or Power BI