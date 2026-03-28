from data_validation_tool.loaders.csv_loader import load_csv
from data_validation_tool.analyzers.counts import (
    count_total,
    count_nulls,
    count_unique,
    count_duplicates,
    count_per_value,
)
from data_validation_tool.analyzers.compare import (
    compare_ids,
    compare_distribution,
)


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

    source_ids = set(bron_df["id"].dropna())
    target_ids = set(doel_df["id"].dropna())

    print(f"Totaal IDs in bron: {len(source_ids)}")
    print(f"Totaal IDs in doel: {len(target_ids)}")

    result = compare_ids(bron_df, doel_df, "id")

    print(f"Overeenkomende IDs: {result['in_both_count']}")
    print(f"Alleen in bron: {result['only_in_source']}")
    print(f"Alleen in doel: {result['only_in_target']}")

    print("\n=== DISTRIBUTIE STATUS ===")

    source_counts, target_counts, diff = compare_distribution(
        bron_df, doel_df, "status"
    )

    print("\nBron:")
    print(source_counts)

    print("\nDoel:")
    print(target_counts)

    print("\nVerschil (doel - bron):")
    for k, v in diff.items():
        print(f"{k}: {v:+}")


if __name__ == "__main__":
    main()
