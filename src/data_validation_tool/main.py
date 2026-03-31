from data_validation_tool.services.single_analysis import run_single_analysis
from data_validation_tool.services.compare_analysis import run_compare_analysis
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

from data_validation_tool.reporting.console import (
    print_compare_summary,
    print_distribution_differences,
    print_row_differences,
    print_single_distributions,
    print_single_summary,
)


def main() -> None:
    """
    Voert de volledige data-validatie uit voor:
    - single dataset analyse
    - vergelijking tussen bron en doel
    - distributieverschillen
    - veldverschillen
    - export van resultaten naar CSV en Excel
    """
    single_result = run_single_analysis(
        file_path=SINGLE_FILE_PATH,
        key_column=KEY_COLUMN,
        distribution_columns=DISTRIBUTION_COLUMNS,
    )

    df = single_result["dataframe"]
    total_records = single_result["total_records"]
    unique_ids = single_result["unique_ids"]
    duplicate_ids = single_result["duplicate_ids"]
    null_counts = single_result["null_counts"]
    distribution_results = single_result["distribution_results"]

    compare_analysis_result = run_compare_analysis(
        source_file_path=SOURCE_FILE_PATH,
        target_file_path=TARGET_FILE_PATH,
        key_column=KEY_COLUMN,
    )

    source_ids = compare_analysis_result["source_ids"]
    target_ids = compare_analysis_result["target_ids"]
    compare_result = compare_analysis_result["compare_result"]
    row_differences = compare_analysis_result["row_differences"]
    distribution_export = compare_analysis_result["distribution_export"]

    print("=== SAMENVATTING ===")

    print_single_summary(
        SINGLE_FILE_PATH,
        KEY_COLUMN,
        total_records,
        unique_ids,
        duplicate_ids,
        null_counts,
    )

    print_compare_summary(
        SOURCE_FILE_PATH,
        TARGET_FILE_PATH,
        KEY_COLUMN,
        source_ids,
        target_ids,
        compare_result,
    )

    print_distribution_differences(distribution_export)

    print_row_differences(row_differences, KEY_COLUMN)

    print_single_distributions(distribution_results)

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
        {
            "categorie": "compare",
            "metric": f"bron_{KEY_COLUMN}s",
            "value": len(source_ids),
        },
        {
            "categorie": "compare",
            "metric": f"doel_{KEY_COLUMN}s",
            "value": len(target_ids),
        },
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

    summary_output_file = "output/summary.csv"
    distribution_output_file = "output/distribution_differences.csv"
    differences_output_file = "output/field_differences.csv"

    export_summary_to_csv(summary_export, summary_output_file)
    export_distribution_to_csv(distribution_export, distribution_output_file)
    export_differences_to_csv(row_differences, differences_output_file)

    print(f"\nCSV export gemaakt: {summary_output_file}")
    print(f"CSV export gemaakt: {distribution_output_file}")
    print(f"CSV export gemaakt: {differences_output_file}")

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
