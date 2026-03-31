import pandas as pd

from src.data_cleaning import clean_readmissions, clean_general_info
from src.transformations import aggregate_readmissions, aggregate_mortality


def main():
    general_info = pd.read_csv("data/raw/hospital_general_info.csv")

    general_info_clean = clean_general_info(general_info)
    general_info_clean.to_csv("data/processed/general_info_clean.csv", index=False)
    print("\n=== CLEANED GENERAL INFO ===")
    print(general_info_clean.head())

    readmissions = clean_readmissions(general_info_clean)
    print("\n=== CLEANED READMISSIONS ===")
    print(readmissions.head())

    aggregated_readmissions = aggregate_readmissions(readmissions)
    print("\n=== AGGREGATED READMISSIONS ===")
    print(aggregated_readmissions.head())
    aggregated_readmissions.to_csv("data/processed/readmissions_clean.csv", index=False)

    aggregated_mortality = aggregate_mortality(general_info_clean)
    print("\n=== AGGREGATED MORTALITY ===")
    print(aggregated_mortality.head())
    aggregated_mortality.to_csv("data/processed/mortality_clean.csv", index=False)


if __name__ == "__main__":
    main()
