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
from data_validation_tool.utils.export import (
    export_differences_to_csv,
    export_distribution_to_csv,
    export_report_to_excel,
    export_summary_to_csv,
)


def main() -> None:
    """
    Voert de volledige data-validatie uit voor:
    - single dataset analyse
    - vergelijking tussen bron en doel
    - distributieverschillen
    - veldverschillen
    - export van resultaten naar CSV
    """
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

    # Verzamel distributieverschillen voor latere export
    distribution_export = []

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

            # Sla distributieverschillen ook op voor export
            for value, difference in non_zero_diff.items():
                distribution_export.append(
                    {
                        "kolom": column,
                        "waarde": value,
                        "verschil_doel_min_bron": difference,
                    }
                )

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
    for value, count in status_counts.items():
        label = "Leeg" if str(value) == "nan" else value
        print(f"- {label}: {count}")

    # Bouw samenvattingsdata op voor export
    summary_export = [
        {"categorie": "single_dataset", "metric": "records", "value": total_records},
        {"categorie": "single_dataset", "metric": "unieke_ids", "value": unique_ids},
        {
            "categorie": "single_dataset",
            "metric": "duplicate_ids",
            "value": duplicate_ids,
        },
        {"categorie": "compare", "metric": "bron_ids", "value": len(source_ids)},
        {"categorie": "compare", "metric": "doel_ids", "value": len(target_ids)},
        {
            "categorie": "compare",
            "metric": "overeenkomende_ids",
            "value": compare_result["in_both_count"],
        },
        {
            "categorie": "compare",
            "metric": "alleen_in_bron",
            "value": str(compare_result["only_in_source"]),
        },
        {
            "categorie": "compare",
            "metric": "alleen_in_doel",
            "value": str(compare_result["only_in_target"]),
        },
        {
            "categorie": "compare",
            "metric": "veldverschillen_aantal",
            "value": len(row_differences),
        },
    ]

    # Exporteer resultaten naar CSV-bestanden
    summary_output_file = "output/summary.csv"
    distribution_output_file = "output/distribution_differences.csv"
    differences_output_file = "output/field_differences.csv"

    export_summary_to_csv(summary_export, summary_output_file)
    export_distribution_to_csv(distribution_export, distribution_output_file)
    export_differences_to_csv(row_differences, differences_output_file)

    print(f"\nCSV export gemaakt: {summary_output_file}")
    print(f"CSV export gemaakt: {distribution_output_file}")
    print(f"CSV export gemaakt: {differences_output_file}")

    # Exporteer één gecombineerd Excel-rapport
    excel_output_file = "output/report.xlsx"
    export_report_to_excel(
        summary_export,
        distribution_export,
        row_differences,
        excel_output_file,
    )

    print(f"Excel export gemaakt: {excel_output_file}")


if __name__ == "__main__":
    main()
