import pandas as pd
import numpy as np


def load_general_info(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_readmissions(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_general_info(df: pd.DataFrame) -> pd.DataFrame:
    key_cols = ["Facility ID", "Facility Name", "State", "Hospital overall rating"]

    df.replace("Not Available", np.nan, inplace=True)

    df = df.assign(
        **{
            "Meets criteria for birthing friendly designation": lambda x: x[
                "Meets criteria for birthing friendly designation"
            ]
            .replace("NaN", np.nan)
            .map({"Y": True})
            .fillna(False)
            .astype(bool)
        }
    )

    mort_cols = [
        "MORT Group Measure Count",
        "Count of Facility MORT Measures",
        "Count of MORT Measures Better",
        "Count of MORT Measures No Different",
        "Count of MORT Measures Worse",
    ]

    safety_cols = [
        "Safety Group Measure Count",
        "Count of Facility Safety Measures",
        "Count of Safety Measures Better",
        "Count of Safety Measures No Different",
        "Count of Safety Measures Worse",
    ]

    te_cols = [ 
        "TE Group Measure Count",
        "Count of Facility TE Measures",
    ]

    ptexp_cols = [
        "Pt Exp Group Measure Count",
        "Count of Facility Pt Exp Measures",
    ]

    df[safety_cols] = df[safety_cols].apply(pd.to_numeric, errors="coerce")
    df[te_cols] = df[te_cols].apply(pd.to_numeric, errors="coerce")
    df[ptexp_cols] = df[ptexp_cols].apply(pd.to_numeric, errors="coerce")
    df[mort_cols] = df[mort_cols].apply(pd.to_numeric, errors="coerce")
    df["Facility ID"] = df["Facility ID"].astype("string")
    df["MORT Group Footnote"] = df["MORT Group Footnote"].astype("string")
    df.dropna(subset=key_cols, inplace=True)
    return df

def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    rm_str = ["Not Availale", "Not Applicable"]
    df = df.replace(rm_str, np.nan)
    df["Patient Survey Star Rating"] = pd.to_numeric(
        df["Patient Survey Star Rating"], errors="coerce"
    )
    df["HCAHPS Linear Mean Value"] = pd.to_numeric(
        df["HCAHPS Linear Mean Value"], errors="coerce"
    )
    return df

def clean_readmissions(df: pd.DataFrame) -> pd.DataFrame:
    readmission_cols = [
        "Facility ID",
        "Facility Name",
        "READM Group Measure Count",
        "Count of Facility READM Measures",
        "Count of READM Measures Better",
        "Count of READM Measures No Different",
        "Count of READM Measures Worse",
    ]

    readmissions = df[readmission_cols].copy()

    readmissions = readmissions.replace(
        ["Not Available", "N/A", "Number of Cases Too Small"], pd.NA
    )

    numeric_cols = [
        "READM Group Measure Count",
        "Count of Facility READM Measures",
        "Count of READM Measures Better",
        "Count of READM Measures No Different",
        "Count of READM Measures Worse",
    ]

    for col in numeric_cols:
        readmissions[col] = pd.to_numeric(readmissions[col], errors="coerce")

    readmissions["Facility ID"] = readmissions["Facility ID"].astype(
        "string"
    ) 
    readmissions["Facility Name"] = readmissions["Facility Name"].astype("string")

    return readmissions

# This function cleans the footnotes data and returns a DataFrame with unique footnote codes and their descriptions
def clean_footnotes(df: pd.DataFrame) -> pd.DataFrame:
    footnotes = (
        df.rename(
            columns={
                "Footnote": "footnote_code",
                "Footnote Text": "footnote_description",
            }
        )[["footnote_code", "footnote_description"]]
        .astype("string")
        .drop_duplicates()
    )
    return footnotes
