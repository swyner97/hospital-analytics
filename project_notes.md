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

### 6. Facility ID Type Consistency _(Updated)_

**Original Decision:**
Facility ID was initially cast to Int64 in some cleaning functions.

**Issue Identified:**
Some Facility IDs may contain non-numeric characters (e.g., 01014F), and casting to integer can either fail or corrupt the data. Additionally, inconsistent typing across tables can cause joins to fail.

**Revised Decision:**
Standardized Facility ID to string across all cleaning functions.

---

### 7. Footnote Code Join: Float-to-String Casting Issue

**Observation:** A bridge table was constructed to link Facility IDs to footnote descriptions via a `footnote_code` key. After casting to string, the merge produced no matches.

**Problem** The "MORT Group Footnote" column was read in as float by pandas due to the presence of NaN values (pandas cannot store NaN in integer columns, so it upcasts to float). Casting to string converted codes like 1 into "1.0", which did not match the clean "1" strings in the footnote crosswalk table.

**Decision** Applied `.str.replace(r"\.0$", "", regex=True).str.strip()` to the bridge table's `footnote_code` column after casting, and `.str.strip()` to the footnote table's code column to guard against whitespace.

>> Additional Findings Most hospitals have no footnote code i.e. the "MORT Group Footnote" column is `NaN` for the majority of facilities. This is expected behavior, not a data error. The merge was confirmed working by filtering for rows where `footnote_code` is not null.

### 8. Bridge Table Helper Refactor

**Observation:** The same bridge-table cleaning logic was being repeated for each CMS footnote category.

**Problem:** Repeating the same code across mortality, readmissions, safety, patient experience, and teaching efficiency makes the pipeline harder to maintain and easier to break.

**Decision:** Created one reusable helper function, build_bridge_footnote(df, footnote_col), that handles:
    - selecting Facility ID and the footnote column
    - renaming to facility_id and footnote_code
    - standardizing ID and code types
    - removing null values
    - dropping duplicate facility-footnote pairs

**Result** The specific bridge functions now only pass in the correct footnote column name, which makes the code cleaner, shorter, and easier to extend.

### 9. Footnote Description Lookup Standardization

**Observation** The bridge tables needed to be joined to the footnote crosswalk table for human-readable descriptions.

**Problem:** Performing separate manual merges for each bridge table duplicated logic and made the pipeline less consistent.

**Decision:** Used a shared helper, attach_footnote_desc(), to merge any bridge table with dim_footnote using the footnote_code key.

**Result:** All footnote bridges now follow the same lookup pattern, and the join logic is centralized in one place.

---

## 10. MultiIndex Columns for HCAHPS Patient Experience Data

**Observation:** The raw HCAHPS dataset contained one row per measure per hospital, with each measure represented as a string ID in the HCAHPS Measure ID column.

**Problem:** The long format made it difficult to compare hospitals across measures and impossible to view a hospital's full performance profile in a single row.

**Decision:** Pivoted the dataset to wide format, one row per hospital, and applied a MultiIndex column structure to group related metrics together.

>> Solution Breakdown:

- Star Ratings and Linear Mean Values were pivoted separately, then concatenated horizontally.
- A measure_map dictionary was used to translate raw CMS measure IDs (e.g., H_COMP_1_STAR_RATING) into human-readable MultiIndex tuples (e.g., ("Nurse Communication", "Star Rating")).
- A `make_multiindex()` helper was defined inside `pivot_ratings()` to apply the mapping cleanly and handle the two identifier columns (Facility Name, Facility ID) which carry no sub-level.
- Columns were explicitly reordered by iterating over measure_map so each Star Rating and Linear Mean pair is adjacent, preventing the measure name from being printed twice when the MultiIndex is rendered.

**Result:** Each hospital occupies one row, with columns grouped by care category and sub-grouped by metric type (Star Rating vs. Linear Mean), making the dataset ready for scoring, ranking, and visualization.

---

## 11. Two Versions of the HCAHPS Pivot Table

**Observation:** The two-level column headers (e.g. Cleanliness → Star Rating / Linear Mean) looked great visually, but will cause problems when trying to do further analysis or save the data to a CSV file. pandas also throws an error when saving a two-level header table to Excel without a row index.

**Problem:** Two-level headers are harder to work with day-to-day. Simple things like selecting a column, merging two tables, or loading the file into another tool all become more complicated than they need to be.

**Decision:** Split the work into two separate functions:

- `pivot_ratings()` — saves a simple, flat table with straightforward column names like `cleanliness_star` and `cleanliness_linear`. This is the version used for all data work and is saved as a CSV.
- `pivot_ratings_display()` — takes that flat table and adds the two-level headers back, but only for the Excel file that is used for viewing and sharing results.

**Result:** The project now produces two output files: a CSV for data work and an Excel file for presentation. All future analysis will use the simple flat CSV, which is much easier to work with.

---

## Next Steps

- Merge with additional CMS datasets (mortality, patient experience)
- Create derived metrics: percentage of measures rated Better vs. Worse, overall performance score
- Statistical analysis: correlation and regression
- Build dashboard in Tableau or Power BI