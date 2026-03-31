import pandas as pd

from src.data_cleaning import clean_footnotes, clean_readmissions, clean_general_info, clean_ratings
from src.transformations import (
    aggregate_readmissions,
    aggregate_mortality,
    aggregate_overall_rating,
    aggregate_safety,
    aggregate_te,
    aggregate_patient_experience,
    build_bridge_mort_footnote,
    build_bridge_ptexp_footnote,
    build_bridge_readm_footnote,
    build_bridge_safety_footnote,
    build_bridge_te_footnote,
    attach_footnote_desc,
    pivot_ratings
)


def main():
    # load
    general_info = pd.read_csv("data/raw/hospital_general_info.csv")
    footnote_crosswalk = pd.read_csv("data/raw/footnote_crosswalk.csv")
    ratings = pd.read_csv("data/raw/HCAHPS_patient_surveys.csv")

    # clean
    general_info_clean = clean_general_info(general_info)
    footnote_dim = clean_footnotes(footnote_crosswalk)
    readmissions_clean = clean_readmissions(general_info_clean)
    pt_ratings_clean = clean_ratings(ratings)

    # transform
    aggregated_readmissions = aggregate_readmissions(readmissions_clean)
    aggregated_mortality = aggregate_mortality(general_info_clean)
    aggregated_safety = aggregate_safety(general_info_clean)
    aggregated_ptexp = aggregate_patient_experience(general_info_clean)
    aggregated_te = aggregate_te(general_info_clean)
    aggregated_rating = aggregate_overall_rating(general_info_clean)
    pivoted_ratings = pivot_ratings(pt_ratings_clean)

    bridge_tables = {
        "mortality": build_bridge_mort_footnote(general_info_clean),
        "readmissions": build_bridge_readm_footnote(general_info_clean),
        "safety": build_bridge_safety_footnote(general_info_clean),
        "patient_exp": build_bridge_ptexp_footnote(general_info_clean),
        "te": build_bridge_te_footnote(general_info_clean),
    }

    # Attach descriptions w helper method
    bridge_with_desc = {
        name: attach_footnote_desc(df, footnote_dim)
        for name, df in bridge_tables.items()
    }

    # save
    general_info_clean.to_csv("data/processed/general_info_clean.csv", index=False)
    footnote_dim.to_csv("data/processed/footnote_dim.csv", index=False)

    aggregated_readmissions.to_csv("data/processed/fact_readmissions.csv", index=False)
    aggregated_mortality.to_csv("data/processed/fact_mortality.csv", index=False)
    aggregated_safety.to_csv("data/processed/fact_safety.csv", index=False)
    aggregated_ptexp.to_csv("data/processed/fact_patient_experience.csv", index=False)
    aggregated_te.to_csv("data/processed/fact_te.csv", index=False)
    aggregated_rating.to_csv("data/processed/fact_overall_rating.csv", index=False)
    pivoted_ratings.to_csv("data/processed/pivot_ratings.csv", index=False)

    for name, df in bridge_tables.items():
        df.to_csv(f"data/processed/bridge_{name}_footnote.csv", index=False)

    # debug and preview outputs
    print("\n=== CLEANED GENERAL INFO ===")
    print(general_info_clean.head())

    print("\n=== FOOTNOTE DIMENSION ===")
    print(footnote_dim.head())

    print("\n=== BRIDGE TABLE CHECKS ===")
    for name, df in bridge_with_desc.items():
        print(f"\n=== {name.upper()} FOOTNOTES ===")
        print(df.dropna(subset=["footnote_code"]).head())


if __name__ == "__main__":
    main()
