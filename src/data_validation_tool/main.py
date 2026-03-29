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

from data_validation_tool.config import (
    SINGLE_FILE_PATH,
    SOURCE_FILE_PATH,
    TARGET_FILE_PATH,
    KEY_COLUMN,
    DISTRIBUTION_COLUMNS,
)

from data_validation_tool.utils.validation import validate_required_column


def main() -> None:
    """
    Voert de volledige data-validatie uit voor:
    - single dataset analyse
    - vergelijking tussen bron en doel
    - distributieverschillen
    - veldverschillen
    - export van resultaten naar CSV en Excel
    """
    df = load_csv(SINGLE_FILE_PATH)
    bron_df = load_csv(SOURCE_FILE_PATH)
    doel_df = load_csv(TARGET_FILE_PATH)

    # Controleer of de key-kolom aanwezig is in alle relevante datasets.
    validate_required_column(df.columns, KEY_COLUMN, "single dataset")
    validate_required_column(bron_df.columns, KEY_COLUMN, "bron")
    validate_required_column(doel_df.columns, KEY_COLUMN, "doel")

    total_records = count_total(df)
    unique_ids = count_unique(df, KEY_COLUMN)
    duplicate_ids = count_duplicates(df, KEY_COLUMN)
    null_counts = count_nulls(df)

    # DISTRIBUTION_COLUMNS zijn optioneel
    distribution_results = {}

    for column in DISTRIBUTION_COLUMNS:
        if column in df.columns:
            distribution_results[column] = count_per_value(df, column)

    source_ids = set(bron_df[KEY_COLUMN].dropna())
    target_ids = set(doel_df[KEY_COLUMN].dropna())

    compare_result = compare_ids(bron_df, doel_df, KEY_COLUMN)
    row_differences = compare_rows(bron_df, doel_df, KEY_COLUMN)

    interesting_columns = get_interesting_columns(
        bron_df,
        max_unique=10,
        exclude_columns=[KEY_COLUMN],
    )

    # Verzamel distributieverschillen voor latere export
    distribution_export = []

    print("=== SAMENVATTING ===")

    print("\nSingle dataset:")
    print(f"- bestand: {SINGLE_FILE_PATH}")
    print(f"- records: {total_records}")
    print(f"- unieke {KEY_COLUMN}s: {unique_ids}")
    print(f"- duplicate {KEY_COLUMN}s: {duplicate_ids}")

    non_zero_nulls = null_counts[null_counts > 0]
    if non_zero_nulls.empty:
        print("- nulls: geen")
    else:
        null_summary = ", ".join(
            f"{column}={count}" for column, count in non_zero_nulls.items()
        )
        print(f"- nulls: {null_summary}")

    print("\nVergelijking bron vs doel:")
    print(f"- bronbestand: {SOURCE_FILE_PATH}")
    print(f"- doelbestand: {TARGET_FILE_PATH}")
    print(f"- bron {KEY_COLUMN}s: {len(source_ids)}")
    print(f"- doel {KEY_COLUMN}s: {len(target_ids)}")
    print(f"- overeenkomende {KEY_COLUMN}s: {compare_result['in_both_count']}")
    print(f"- alleen in bron: {compare_result['only_in_source']}")
    print(f"- alleen in doel: {compare_result['only_in_target']}")

    print("\nDistributieverschillen:")
    found_distribution_difference = False

    for column in interesting_columns:
        _, _, diff = compare_distribution(bron_df, doel_df, column)

        non_zero_diff = {
            value: difference
            for value, difference in diff.items()
            if difference != 0
        }

        if non_zero_diff:
            found_distribution_difference = True
            diff_summary = ", ".join(
                f"{value} {difference:+}"
                for value, difference in non_zero_diff.items()
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
                f"  - {KEY_COLUMN} {diff['key']} | {diff['kolom']} | "
                f"{diff['bron']} -> {diff['doel']}"
            )

    print("\nDetails single dataset:")

    if distribution_results:
        for column, counts in distribution_results.items():
            print(f"\nVerdeling van {column}:")
            for value, count in counts.items():
                label = "Leeg" if str(value) == "nan" else value
                print(f"- {label}: {count}")
    else:
        print("- Geen distributiekolommen geconfigureerd of gevonden")

    # Bouw samenvattingsdata op voor export
    summary_export = [
        {"categorie": "single_dataset", "metric": "bestand", "value": SINGLE_FILE_PATH},
        {"categorie": "single_dataset", "metric": "records", "value": total_records},
        {
            "categorie": "single_dataset",
            "metric": f"unieke_{KEY_COLUMN}s",
            "value": unique_ids,
        },
        {
            "categorie": "single_dataset",
            "metric": f"duplicate_{KEY_COLUMN}s",
            "value": duplicate_ids,
        },
        {"categorie": "compare", "metric": "bronbestand", "value": SOURCE_FILE_PATH},
        {"categorie": "compare", "metric": "doelbestand", "value": TARGET_FILE_PATH},
        {"categorie": "compare", "metric": f"bron_{KEY_COLUMN}s", "value": len(source_ids)},
        {"categorie": "compare", "metric": f"doel_{KEY_COLUMN}s", "value": len(target_ids)},
        {
            "categorie": "compare",
            "metric": f"overeenkomende_{KEY_COLUMN}s",
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

    # Exporteer daarnaast één gecombineerd Excel-rapport
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