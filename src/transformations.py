import pandas as pd


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
