import pandas as pd


def load_general_info(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


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

    # Replace known bad values BEFORE conversion
    readmissions = readmissions.replace(
        ["Not Available", "N/A", "Number of Cases Too Small"], pd.NA
    )

    numeric_cols = [
        "Facility ID",
        "READM Group Measure Count",
        "Count of Facility READM Measures",
        "Count of READM Measures Better",
        "Count of READM Measures No Different",
        "Count of READM Measures Worse",
    ]

    # Force numeric conversion
    for col in numeric_cols:
        readmissions[col] = pd.to_numeric(readmissions[col], errors="coerce")

    # Set final types
    readmissions["Facility ID"] = readmissions["Facility ID"].astype("Int64")
    readmissions["Facility Name"] = readmissions["Facility Name"].astype("string")

    return readmissions
