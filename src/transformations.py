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


def attach_footnote_desc(
    bridge: pd.DataFrame, dim_footnote: pd.DataFrame
) -> pd.DataFrame:
    return bridge.merge(dim_footnote, on="footnote_code", how="left")
