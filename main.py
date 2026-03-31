import pandas as pd

from src.data_cleaning import clean_footnotes, clean_readmissions, clean_general_info
from src.transformations import (
    aggregate_readmissions,
    aggregate_mortality,
    build_bridge_mort_footnote,
    attach_footnote_desc
)


def main():
    # load
    general_info = pd.read_csv("data/raw/hospital_general_info.csv")
    footnote_crosswalk = pd.read_csv("data/raw/footnote_crosswalk.csv")

    # clean
    general_info_clean = clean_general_info(general_info)
    footnote_dim = clean_footnotes(footnote_crosswalk)
    readmissions_clean = clean_readmissions(general_info_clean)

    # transform
    aggregated_readmissions = aggregate_readmissions(readmissions_clean)
    aggregated_mortality = aggregate_mortality(general_info_clean)
    bridge_mort_footnote = build_bridge_mort_footnote(general_info_clean)

    # preview join for checking
    bridge_with_desc = bridge_mort_footnote.merge(
        footnote_dim, on="footnote_code", how="left"
    )

    # save
    general_info_clean.to_csv("data/processed/general_info_clean.csv", index=False)
    footnote_dim.to_csv("data/processed/footnote_dim.csv", index=False)
    bridge_mort_footnote.to_csv("data/processed/bridge_mort_footnote.csv", index=False)
    aggregated_readmissions.to_csv("data/processed/readmissions_clean.csv", index=False)
    aggregated_mortality.to_csv("data/processed/mortality_clean.csv", index=False)

    print("\n=== CLEANED GENERAL INFO ===")
    print(general_info_clean.head())

    print("\n=== FOOTNOTE DIMENSION ===")
    print(footnote_dim.head())

    print("\n=== BRIDGE TABLE ===")
    print(bridge_mort_footnote.head())

    print("\n=== BRIDGE WITH DESCRIPTIONS ===")
    print(bridge_with_desc.dropna(subset=["footnote_code"]).head())


if __name__ == "__main__":
    main()
