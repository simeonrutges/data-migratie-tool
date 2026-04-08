from data_validation_tool.analyzers.compare import (
    compare_distribution,
    compare_ids,
    compare_rows,
    get_interesting_columns,
)
from data_validation_tool.loaders.file_loader import load_file
from data_validation_tool.utils.validation import validate_required_column


def run_compare_analysis(
    source_file_path: str,
    target_file_path: str,
    key_column: str,
) -> dict:
    """
    Voert een vergelijking uit tussen bron- en doeldataset.

    Ondersteunde bestandstypen:
    - CSV
    - Excel (.xlsx)
    - JSON

    Parameters:
    - source_file_path: pad naar bronbestand
    - target_file_path: pad naar doelbestand
    - key_column: kolom die gebruikt wordt om records te koppelen

    Returns:
    - dict met alle resultaten van de compare-analyse
    """
    bron_df = load_file(source_file_path)
    doel_df = load_file(target_file_path)

    # De key-kolom is verplicht voor een geldige vergelijking.
    validate_required_column(bron_df.columns, key_column, "bron")
    validate_required_column(doel_df.columns, key_column, "doel")

    source_ids = set(bron_df[key_column].dropna())
    target_ids = set(doel_df[key_column].dropna())

    compare_result = compare_ids(bron_df, doel_df, key_column)
    row_differences = compare_rows(bron_df, doel_df, key_column)

    interesting_columns = get_interesting_columns(
        bron_df,
        max_unique=10,
        exclude_columns=[key_column],
    )

    distribution_export = []

    for column in interesting_columns:
        _, _, diff = compare_distribution(bron_df, doel_df, column)

        non_zero_diff = {
            value: difference for value, difference in diff.items() if difference != 0
        }

        # Alleen echte verschillen opslaan voor rapportage en export.
        for value, difference in non_zero_diff.items():
            distribution_export.append(
                {
                    "kolom": column,
                    "waarde": value,
                    "verschil_doel_min_bron": difference,
                }
            )

    return {
        "bron_df": bron_df,
        "doel_df": doel_df,
        "source_ids": source_ids,
        "target_ids": target_ids,
        "compare_result": compare_result,
        "row_differences": row_differences,
        "distribution_export": distribution_export,
    }
