# from data_validation_tool.loaders.csv_loader import load_csv
# from data_validation_tool.analyzers.counts import (
#     count_total,
#     count_nulls,
#     count_unique,
#     count_duplicates,
#     count_per_value,
# )
# from data_validation_tool.analyzers.compare import (
#     compare_ids,
#     compare_distribution,
#     compare_rows,
#     get_interesting_columns,
# )


# def main() -> None:
#     df = load_csv("data/single/example.csv")

#     print("=== BASIS ANALYSE ===")
#     print(f"Totaal aantal records: {count_total(df)}")
#     print(f"Aantal unieke IDs: {count_unique(df, 'id')}")
#     print(f"Aantal duplicate IDs: {count_duplicates(df, 'id')}")
#     print("\nNulls per kolom:")
#     print(count_nulls(df))
#     print("\nAantal per status:")
#     print(count_per_value(df, "status"))

#     bron_df = load_csv("data/compare/bron.csv")
#     doel_df = load_csv("data/compare/doel.csv")

#     print("\nKolommen in bron:")
#     print(bron_df.columns)

#     print("\n=== VERGELIJKING BRON VS DOEL ===")

#     source_ids = set(bron_df["id"].dropna())
#     target_ids = set(doel_df["id"].dropna())

#     print(f"Totaal IDs in bron: {len(source_ids)}")
#     print(f"Totaal IDs in doel: {len(target_ids)}")

#     result = compare_ids(bron_df, doel_df, "id")

#     print(f"Overeenkomende IDs: {result['in_both_count']}")
#     print(f"Alleen in bron: {result['only_in_source']}")
#     print(f"Alleen in doel: {result['only_in_target']}")

#     print("\n=== DISTRIBUTIE VERGELIJKING ===")

#     interesting_columns = get_interesting_columns(
#         bron_df,
#         max_unique=10,
#         exclude_columns=["id"],
#     )

#     print(f"Interessante kolommen: {interesting_columns}")

#     for column in interesting_columns:
#         print(f"\n--- Kolom: {column} ---")

#     source_counts, target_counts, diff = compare_distribution(bron_df, doel_df, column)

#     print("\nBron:")
#     print(source_counts)

#     print("\nDoel:")
#     print(target_counts)

#     print("\nVerschil (doel - bron):")
#     for value, difference in diff.items():
#         print(f"{value}: {difference:+}")

#     print("\n=== VELD-VERSCHILLEN ===")

#     row_differences = compare_rows(bron_df, doel_df, "id")

#     if not row_differences:
#         print("Geen veldverschillen gevonden.")
#     else:
#         for diff in row_differences:
#             print(
#                 f"ID {diff['id']} - kolom '{diff['kolom']}': "
#                 f"bron='{diff['bron']}' -> doel='{diff['doel']}'"
#             )


# if __name__ == "__main__":
#     main()

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
    compare_rows,
    get_interesting_columns,
)


def main() -> None:
    df = load_csv("data/single/example.csv")

    total_records = count_total(df)
    unique_ids = count_unique(df, "id")
    duplicate_ids = count_duplicates(df, "id")
    null_counts = count_nulls(df)
    status_counts = count_per_value(df, "status")

    bron_df = load_csv("data/compare/bron.csv")
    doel_df = load_csv("data/compare/doel.csv")

    source_ids = set(bron_df["id"].dropna())
    target_ids = set(doel_df["id"].dropna())

    compare_result = compare_ids(bron_df, doel_df, "id")
    row_differences = compare_rows(bron_df, doel_df, "id")

    interesting_columns = get_interesting_columns(
        bron_df,
        max_unique=10,
        exclude_columns=["id"],
    )

    print("=== SAMENVATTING ===")

    print("\nSingle dataset:")
    print(f"- records: {total_records}")
    print(f"- unieke IDs: {unique_ids}")
    print(f"- duplicate IDs: {duplicate_ids}")

    non_zero_nulls = null_counts[null_counts > 0]
    if non_zero_nulls.empty:
        print("- nulls: geen")
    else:
        null_summary = ", ".join(
            f"{column}={count}" for column, count in non_zero_nulls.items()
        )
        print(f"- nulls: {null_summary}")

    print("\nVergelijking bron vs doel:")
    print(f"- bron IDs: {len(source_ids)}")
    print(f"- doel IDs: {len(target_ids)}")
    print(f"- overeenkomende IDs: {compare_result['in_both_count']}")
    print(f"- alleen in bron: {compare_result['only_in_source']}")
    print(f"- alleen in doel: {compare_result['only_in_target']}")

    print("\nDistributieverschillen:")
    found_distribution_difference = False

    for column in interesting_columns:
        _, _, diff = compare_distribution(bron_df, doel_df, column)

        non_zero_diff = {
            value: difference for value, difference in diff.items() if difference != 0
        }

        if non_zero_diff:
            found_distribution_difference = True
            diff_summary = ", ".join(
                f"{value} {difference:+}" for value, difference in non_zero_diff.items()
            )
            print(f"- {column}: {diff_summary}")

    if not found_distribution_difference:
        print("- geen distributieverschillen gevonden")

    print("\nVeldverschillen:")
    if not row_differences:
        print("- geen veldverschillen gevonden")
    else:
        print(f"- {len(row_differences)} verschil(len) gevonden")
        for diff in row_differences:
            print(
                f"  - ID {diff['id']} | {diff['kolom']} | "
                f"{diff['bron']} -> {diff['doel']}"
            )

    print("\nDetails single dataset:")
    print("\nStatusverdeling:")
    print(status_counts)


if __name__ == "__main__":
    main()
