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

    df[mort_cols] = df[mort_cols].apply(pd.to_numeric, errors="coerce")
    df["Facility ID"] = df["Facility ID"].astype("string")
    df.dropna(subset=key_cols, inplace=True)
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
