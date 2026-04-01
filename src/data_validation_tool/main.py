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
    MODE,
)

from data_validation_tool.reporting.console import (
    print_compare_summary,
    print_distribution_differences,
    print_row_differences,
    print_single_distributions,
    print_single_summary,
)

from data_validation_tool.reporting.summary import build_summary_export

# def main() -> None:
#     """
#     Voert de volledige data-validatie uit voor:
#     - single dataset analyse
#     - vergelijking tussen bron en doel
#     - distributieverschillen
#     - veldverschillen
#     - export van resultaten naar CSV en Excel
#     """
#     single_result = run_single_analysis(
#         file_path=SINGLE_FILE_PATH,
#         key_column=KEY_COLUMN,
#         distribution_columns=DISTRIBUTION_COLUMNS,
#     )

#     total_records = single_result["total_records"]
#     unique_ids = single_result["unique_ids"]
#     duplicate_ids = single_result["duplicate_ids"]
#     null_counts = single_result["null_counts"]
#     distribution_results = single_result["distribution_results"]

#     compare_analysis_result = run_compare_analysis(
#         source_file_path=SOURCE_FILE_PATH,
#         target_file_path=TARGET_FILE_PATH,
#         key_column=KEY_COLUMN,
#     )

#     source_ids = compare_analysis_result["source_ids"]
#     target_ids = compare_analysis_result["target_ids"]
#     compare_result = compare_analysis_result["compare_result"]
#     row_differences = compare_analysis_result["row_differences"]
#     distribution_export = compare_analysis_result["distribution_export"]

#     print("=== SAMENVATTING ===")

#     print_single_summary(
#         SINGLE_FILE_PATH,
#         KEY_COLUMN,
#         total_records,
#         unique_ids,
#         duplicate_ids,
#         null_counts,
#     )

#     print_compare_summary(
#         SOURCE_FILE_PATH,
#         TARGET_FILE_PATH,
#         KEY_COLUMN,
#         source_ids,
#         target_ids,
#         compare_result,
#     )

#     print_distribution_differences(distribution_export)

#     print_row_differences(row_differences, KEY_COLUMN)

#     print_single_distributions(distribution_results)

#     summary_export = build_summary_export(
#     single_file_path=SINGLE_FILE_PATH,
#     source_file_path=SOURCE_FILE_PATH,
#     target_file_path=TARGET_FILE_PATH,
#     key_column=KEY_COLUMN,
#     total_records=total_records,
#     unique_ids=unique_ids,
#     duplicate_ids=duplicate_ids,
#     source_ids=source_ids,
#     target_ids=target_ids,
#     compare_result=compare_result,
#     row_differences=row_differences,
#     )

#     summary_output_file = "output/summary.csv"
#     distribution_output_file = "output/distribution_differences.csv"
#     differences_output_file = "output/field_differences.csv"

#     export_summary_to_csv(summary_export, summary_output_file)
#     export_distribution_to_csv(distribution_export, distribution_output_file)
#     export_differences_to_csv(row_differences, differences_output_file)

#     print(f"\nCSV export gemaakt: {summary_output_file}")
#     print(f"CSV export gemaakt: {distribution_output_file}")
#     print(f"CSV export gemaakt: {differences_output_file}")

#     excel_output_file = "output/report.xlsx"
#     export_report_to_excel(
#         summary_export,
#         distribution_export,
#         row_differences,
#         excel_output_file,
#     )

#     print(f"Excel export gemaakt: {excel_output_file}")


def main() -> None:
    """
    Voert data-validatie uit in één van de volgende modi:
    - single
    - compare
    - all
    """
    print("=== SAMENVATTING ===")

    summary_export = []
    distribution_export = []
    row_differences = []

    # Variabelen alvast initialiseren zodat export later veilig blijft werken.
    total_records = 0
    unique_ids = 0
    duplicate_ids = 0
    null_counts = None
    distribution_results = {}

    source_ids = set()
    target_ids = set()
    compare_result = {
        "in_both_count": 0,
        "only_in_source": [],
        "only_in_target": [],
    }

    if MODE in ["all", "single"]:
        single_result = run_single_analysis(
            file_path=SINGLE_FILE_PATH,
            key_column=KEY_COLUMN,
            distribution_columns=DISTRIBUTION_COLUMNS,
        )

        total_records = single_result["total_records"]
        unique_ids = single_result["unique_ids"]
        duplicate_ids = single_result["duplicate_ids"]
        null_counts = single_result["null_counts"]
        distribution_results = single_result["distribution_results"]

        print_single_summary(
            SINGLE_FILE_PATH,
            KEY_COLUMN,
            total_records,
            unique_ids,
            duplicate_ids,
            null_counts,
        )

        print_single_distributions(distribution_results)

    if MODE in ["all", "compare"]:
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

    if MODE not in ["single", "compare", "all"]:
        raise ValueError(
            f"Ongeldige MODE: '{MODE}'. Gebruik 'single', 'compare' of 'all'."
        )

    summary_export = build_summary_export(
        single_file_path=SINGLE_FILE_PATH,
        source_file_path=SOURCE_FILE_PATH,
        target_file_path=TARGET_FILE_PATH,
        key_column=KEY_COLUMN,
        total_records=total_records,
        unique_ids=unique_ids,
        duplicate_ids=duplicate_ids,
        source_ids=source_ids,
        target_ids=target_ids,
        compare_result=compare_result,
        row_differences=row_differences,
    )

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
