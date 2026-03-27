from data_migration_tool.loaders.csv_loader import load_csv
from data_migration_tool.analyzers.counts import (
    count_total,
    count_nulls,
    count_unique,
    count_duplicates,
)


def main() -> None:
    df = load_csv("data/example.csv")

    print("=== BASIS ANALYSE ===")
    print(f"Totaal aantal records: {count_total(df)}")
    print(f"Aantal unieke IDs: {count_unique(df, 'id')}")
    print(f"Aantal duplicate IDs: {count_duplicates(df, 'id')}")
    print("\nNulls per kolom:")
    print(count_nulls(df))


if __name__ == "__main__":
    main()