import pandas as pd


def aggregate_mortality(df: pd.DataFrame) -> pd.DataFrame:
    df["MORT Net Score"] = (
        df["Count of MORT Measures Better"] - df["Count of MORT Measures Worse"]
    ) / df["Count of Facility MORT Measures"]

    aggregated = (
        df.groupby(["Facility ID", "Facility Name"])
        .agg(MORT_Net_Score=("MORT Net Score", "mean"))
        .round(2)
        .reset_index()
        .sort_values("MORT_Net_Score", ascending=False)
    )
    return aggregated


def aggregate_readmissions(df: pd.DataFrame) -> pd.DataFrame:
    df["READM Net Score"] = (
        df["Count of READM Measures Better"] - df["Count of READM Measures Worse"]
    ) / df["Count of Facility READM Measures"]
    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
                "READM Net Score": "mean",
                "READM Group Measure Count": "max",
                "Count of Facility READM Measures": "sum",
                "Count of READM Measures Better": "sum",
                "Count of READM Measures No Different": "sum",
                "Count of READM Measures Worse": "sum",
            }
        )
        .reset_index()
    )

    return aggregated


def aggregate_overall_rating(df: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
                "Hospital overall rating": "max",
            }
        )
        .reset_index()
    )

    return aggregated


def aggregate_safety(df: pd.DataFrame) -> pd.DataFrame:
    df["Safety Net Score"] = (
        df["Count of Safety Measures Better"] - df["Count of Safety Measures Worse"]
    ) / df["Count of Facility Safety Measures"]

    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
                "Safety Group Measure Count": "max",
                "Count of Facility Safety Measures": "sum",
                "Count of Safety Measures Better": "sum",
                "Count of Safety Measures No Different": "sum",
                "Count of Safety Measures Worse": "sum",
            }
        )
        .reset_index()
    )

    return aggregated


def aggregate_patient_experience(df: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
                "Pt Exp Group Measure Count": "max",
                "Count of Facility Pt Exp Measures": "sum",
            }
        )
        .reset_index()
    )

    return aggregated


def aggregate_te(df: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
                "TE Group Measure Count": "max",
                "Count of Facility TE Measures": "sum",
            }
        )
        .reset_index()
    )

    return aggregated


def build_bridge_footnote(
    df: pd.DataFrame,
    footnote_col: str,
) -> pd.DataFrame:
    """
    Build a bridge table with one row per facility-footnote relationship.
    """
    bridge = df[["Facility ID", footnote_col]].copy()

    bridge = bridge.rename(
        columns={
            "Facility ID": "facility_id",
            footnote_col: "footnote_code",
        }
    )

    bridge["facility_id"] = pd.to_numeric(
        bridge["facility_id"], errors="coerce"
    ).astype("Int64")
    bridge["footnote_code"] = (
        bridge["footnote_code"]
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )

    bridge = bridge.dropna(subset=["facility_id", "footnote_code"])
    bridge = bridge.drop_duplicates(subset=["facility_id", "footnote_code"])

    return bridge


def build_bridge_mort_footnote(df: pd.DataFrame) -> pd.DataFrame:
    return build_bridge_footnote(df, "MORT Group Footnote")


def build_bridge_safety_footnote(df: pd.DataFrame) -> pd.DataFrame:
    return build_bridge_footnote(df, "Safety Group Footnote")


def build_bridge_readm_footnote(df: pd.DataFrame) -> pd.DataFrame:
    return build_bridge_footnote(df, "READM Group Footnote")


def build_bridge_ptexp_footnote(df: pd.DataFrame) -> pd.DataFrame:
    return build_bridge_footnote(df, "Pt Exp Group Footnote")


def build_bridge_te_footnote(df: pd.DataFrame) -> pd.DataFrame:
    return build_bridge_footnote(df, "TE Group Footnote")


def build_dim_footnote(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["footnote_code"] = (
        df["footnote_code"]
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )

    df = df.dropna(subset=["footnote_code"])
    df = df.drop_duplicates(subset=["footnote_code"])

    return df


def attach_footnote_desc(
    bridge: pd.DataFrame, dim_footnote: pd.DataFrame
) -> pd.DataFrame:
    return bridge.merge(dim_footnote, on="footnote_code", how="left")


def pivot_ratings(df: pd.DataFrame) -> pd.DataFrame:
    measure_map = {
        "H_CLEAN_STAR_RATING": ("Cleanliness", "Star Rating"),
        "H_CLEAN_LINEAR_SCORE": ("Cleanliness", "Linear Mean"),
        "H_COMP_1_STAR_RATING": ("Nurse Communication", "Star Rating"),
        "H_COMP_1_LINEAR_SCORE": ("Nurse Communication", "Linear Mean"),
        "H_COMP_2_STAR_RATING": ("Doctor Communication", "Star Rating"),
        "H_COMP_2_LINEAR_SCORE": ("Doctor Communication", "Linear Mean"),
        "H_COMP_3_STAR_RATING": ("Responsiveness of Hospital Staff", "Star Rating"),
        "H_COMP_3_LINEAR_SCORE": ("Responsiveness of Hospital Staff", "Linear Mean"),
        "H_COMP_4_STAR_RATING": ("Pain Management", "Star Rating"),
        "H_COMP_4_LINEAR_SCORE": ("Pain Management", "Linear Mean"),
        "H_COMP_5_STAR_RATING": ("Communication about Medicines", "Star Rating"),
        "H_COMP_5_LINEAR_SCORE": ("Communication about Medicines", "Linear Mean"),
        "H_COMP_6_STAR_RATING": ("Discharge Information", "Star Rating"),
        "H_COMP_6_LINEAR_SCORE": ("Discharge Information", "Linear Mean"),
        "H_QUIET_STAR_RATING": ("Quietness", "Star Rating"),
        "H_QUIET_LINEAR_SCORE": ("Quietness", "Linear Mean"),
        "H_HSP_RATING_STAR_RATING": ("Overall Hospital Rating", "Star Rating"),
        "H_HSP_RATING_LINEAR_SCORE": ("Overall Hospital Rating", "Linear Mean"),
        "H_RECMND_STAR_RATING": ("Recommend Hospital", "Star Rating"),
        "H_RECMND_LINEAR_SCORE": ("Recommend Hospital", "Linear Mean"),
    }

    df = df[df["HCAHPS Measure ID"].isin(measure_map.keys())].copy()

    star = df[df["HCAHPS Measure ID"].str.contains("STAR_RATING")].pivot_table(
        index=["Facility ID", "Facility Name"],
        columns="HCAHPS Measure ID",
        values="Patient Survey Star Rating",
    )

    linear = df[df["HCAHPS Measure ID"].str.contains("LINEAR")].pivot_table(
        index=["Facility ID", "Facility Name"],
        columns="HCAHPS Measure ID",
        values="HCAHPS Linear Mean Value",
    )

    df = pd.concat([star, linear], axis=1).reset_index()

    # order columns so each star/linear pair is adjacent
    ordered_cols = ["Facility ID", "Facility Name"]
    for key in measure_map:
        if key in df.columns:
            ordered_cols.append(key)

    df = df[ordered_cols]

    # flatten column names into readable snake_case strings
    def flatten_col(col):
        if col in ("Facility ID", "Facility Name"):
            return col
        measure, sub = measure_map[col]
        suffix = "star" if "Star" in sub else "linear"
        return f"{measure.lower().replace(' ', '_')}_{suffix}"

    df.columns = [flatten_col(c) for c in df.columns]

    return df


def pivot_ratings_display(df: pd.DataFrame) -> pd.DataFrame:
    # map flat column names back to (measure, sub-column) tuples for the multiindex
    col_map = {
        "cleanliness_star": ("Cleanliness", "Star Rating"),
        "cleanliness_linear": ("Cleanliness", "Linear Mean"),
        "nurse_communication_star": ("Nurse Communication", "Star Rating"),
        "nurse_communication_linear": ("Nurse Communication", "Linear Mean"),
        "doctor_communication_star": ("Doctor Communication", "Star Rating"),
        "doctor_communication_linear": ("Doctor Communication", "Linear Mean"),
        "responsiveness_of_hospital_staff_star": (
            "Responsiveness of Hospital Staff",
            "Star Rating",
        ),
        "responsiveness_of_hospital_staff_linear": (
            "Responsiveness of Hospital Staff",
            "Linear Mean",
        ),
        "pain_management_star": ("Pain Management", "Star Rating"),
        "pain_management_linear": ("Pain Management", "Linear Mean"),
        "communication_about_medicines_star": (
            "Communication about Medicines",
            "Star Rating",
        ),
        "communication_about_medicines_linear": (
            "Communication about Medicines",
            "Linear Mean",
        ),
        "discharge_information_star": ("Discharge Information", "Star Rating"),
        "discharge_information_linear": ("Discharge Information", "Linear Mean"),
        "quietness_star": ("Quietness", "Star Rating"),
        "quietness_linear": ("Quietness", "Linear Mean"),
        "overall_hospital_rating_star": ("Overall Hospital Rating", "Star Rating"),
        "overall_hospital_rating_linear": ("Overall Hospital Rating", "Linear Mean"),
        "recommend_hospital_star": ("Recommend Hospital", "Star Rating"),
        "recommend_hospital_linear": ("Recommend Hospital", "Linear Mean"),
    }

    # build multiIndex tuples, leaving facility ID and name as top-level only
    tuples = []
    for col in df.columns:
        if col in ("Facility ID", "Facility Name"):
            tuples.append((col, ""))
        else:
            tuples.append(col_map.get(col, (col, "")))

    df = df.copy()
    df.columns = pd.MultiIndex.from_tuples(tuples)

    return df
