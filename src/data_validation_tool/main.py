from data_validation_tool.loaders.csv_loader import load_csv
from data_validation_tool.analyzers.counts import (
    count_total,
    count_nulls,
    count_unique,
    count_duplicates,
    count_per_value,
)
from data_validation_tool.analyzers.compare import compare_ids


def main() -> None:
    df = load_csv("data/single/example.csv")

    print("=== BASIS ANALYSE ===")
    print(f"Totaal aantal records: {count_total(df)}")
    print(f"Aantal unieke IDs: {count_unique(df, 'id')}")
    print(f"Aantal duplicate IDs: {count_duplicates(df, 'id')}")
    print("\nNulls per kolom:")
    print(count_nulls(df))
    print("\nAantal per status:")
    print(count_per_value(df, "status"))

    bron_df = load_csv("data/compare/bron.csv")
    doel_df = load_csv("data/compare/doel.csv")

    print("\n=== VERGELIJKING BRON VS DOEL ===")
    result = compare_ids(bron_df, doel_df, "id")
    print(f"Aantal IDs in beide bestanden: {result['in_both_count']}")
    print(f"Alleen in bron: {result['only_in_source']}")
    print(f"Alleen in doel: {result['only_in_target']}")


if __name__ == "__main__":
    main()