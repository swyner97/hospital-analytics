from src.data_cleaning import load_general_info, clean_readmissions
from src.transformations import aggregate_readmissions


def main():
    path = "data/raw/hospital_general_info.csv"

    df = load_general_info(path)
    print("\n=== RAW DATA ===")
    print(df.head())

    readmissions = clean_readmissions(df)
    print("\n=== CLEANED READMISSIONS ===")
    print(readmissions.head())

    aggregated = aggregate_readmissions(readmissions)
    print("\n=== AGGREGATED ===")
    print(aggregated.head())
    aggregated.to_csv("data/processed/readmissions_clean.csv", index=False)


if __name__ == "__main__":
    main()
