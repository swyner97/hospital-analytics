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

### 5. Mortality Net Score

**Observation:** The mortality dataset contained raw counts for measures rated Better, Worse, and No Different relative to national benchmarks.

**Problem:** Raw counts are not comparable across hospitals since some hospitals have more measures than others.

**Decision:** Calculated a net score — (Better − Worse) / Total Measures — to normalize performance into a single comparable value per hospital. A positive score indicates more measures performing above the national average; a negative score indicates more performing below.

**Solution breakdown:**
- Individual rate columns (Better Rate, Worse Rate, No Different Rate) were dropped since they are redundant when the goal is ranking.
- Net score was rounded to 2 decimal places for readability.
- Hospitals were sorted descending by net score so the best performers appear first.

---

### 6. Facility ID Type Consistency

**Observation:** Facility ID was being cast to `Int64` in readmissions cleaning but `string` in general info cleaning.

**Problem:** Inconsistent types on a join key cause merges to silently fail or produce nulls.

**Decision:** Standardized Facility ID to `string` across all cleaning functions. Some IDs contain non-numeric characters (e.g. `01014F`), making integer casting invalid regardless.

---

### 7. Footnote Code Join: Float-to-String Casting Issue

**Observation** A bridge table was constructed to link Facility IDs to footnote descriptions via a `footnote_code` key. After casting to string, the merge produced no matches.

**Problem** The "MORT Group Footnote" column was read in as float by pandas due to the presence of NaN values (pandas cannot store NaN in integer columns, so it upcasts to float). Casting to string converted codes like 1 into "1.0", which did not match the clean "1" strings in the footnote crosswalk table.

**Decision** Applied `.str.replace(r"\.0$", "", regex=True).str.strip()` to the bridge table's `footnote_code` column after casting, and `.str.strip()` to the footnote table's code column to guard against whitespace.

>> Additional Findings Most hospitals have no footnote code i.e.the "MORT Group Footnote" column is `NaN` for the majority of facilities. This is expected behavior, not a data error. The merge was confirmed working by filtering for rows where `footnote_code` is not null.

## Next Steps

- Merge with additional CMS datasets (mortality, patient experience)
- Create derived metrics: percentage of measures rated Better vs. Worse, overall performance score
- Statistical analysis: correlation and regression
- Build dashboard in Tableau or Power BI