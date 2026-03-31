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
    aggregated = (
        df.groupby("Facility ID")
        .agg(
            {
                "Facility Name": "first",
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


# This function creates a bridge table to link mortality measures with their corresponding footnotes
def build_bridge_mort_footnote(df: pd.DataFrame) -> pd.DataFrame:
    bridge = (
        df[["Facility ID", "MORT Group Footnote"]]
        .copy()
        .astype("string")
        .rename(
            columns={
                "Facility ID": "facility_id",
                "MORT Group Footnote": "footnote_code",
            }
        )
    )
    bridge["footnote_code"] = (
        bridge["footnote_code"].str.replace(r"\.0$", "", regex=True).str.strip()
    )
    return bridge

def build_bridge_safety_footnote(df: pd.DataFrame) -> pd.DataFrame:
    bridge = (
        df[["Facility ID", "Safety Group Footnote"]]
        .copy()
        .astype("string")
        .rename(
            columns={
                "Facility ID": "facility_id",
                "Safety Group Footnote": "footnote_code",
            }
        )
    )
    bridge["footnote_code"] = (
        bridge["footnote_code"].str.replace(r"\.0$", "", regex=True).str.strip()
    )
    return bridge

def build_bridge_readm_footnote(df: pd.DataFrame) -> pd.DataFrame:
    bridge = (
        df[["Facility ID", "READM Group Footnote"]]
        .copy()
        .astype("string")
        .rename(
            columns={
                "Facility ID": "facility_id",
                "READM Group Footnote": "footnote_code",
            }
        )
    )
    bridge["footnote_code"] = (
        bridge["footnote_code"].str.replace(r"\.0$", "", regex=True).str.strip()
    )
    return bridge

def build_bridge_ptexp_footnote(df: pd.DataFrame) -> pd.DataFrame:
    bridge = (
        df[["Facility ID", "Pt Exp Group Footnote"]]
        .copy()
        .astype("string")
        .rename(
            columns={
                "Facility ID": "facility_id",
                "Pt Exp Group Footnote": "footnote_code",
            }
        )
    )
    bridge["footnote_code"] = (
        bridge["footnote_code"].str.replace(r"\.0$", "", regex=True).str.strip()
    )
    return bridge

def build_bridge_te_footnote(df: pd.DataFrame) -> pd.DataFrame:
    bridge = (
        df[["Facility ID", "TE Group Footnote"]]
        .copy()
        .astype("string")
        .rename(
            columns={
                "Facility ID": "facility_id",
                "TE Group Footnote": "footnote_code",
            }
        )
    )
    bridge["footnote_code"] = (
        bridge["footnote_code"].str.replace(r"\.0$", "", regex=True).str.strip()
    )
    return bridge

def attach_footnote_desc(
    bridge: pd.DataFrame, dim_footnote: pd.DataFrame
) -> pd.DataFrame:
    return bridge.merge(dim_footnote, on="footnote_code", how="left")
