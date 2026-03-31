from data_validation_tool.analyzers.counts import (
    count_duplicates,
    count_nulls,
    count_per_value,
    count_total,
    count_unique,
)
from data_validation_tool.loaders.csv_loader import load_csv


def run_single_analysis(
    file_path: str,
    key_column: str,
    distribution_columns: list[str],
) -> dict:
    """
    Voert een single dataset analyse uit op één bestand.

    Parameters:
    - file_path: pad naar het inputbestand
    - key_column: kolom die gebruikt wordt als unieke sleutel
    - distribution_columns: kolommen waarvan een waardeverdeling getoond moet worden

    Returns:
    - dict met alle resultaten van de single analyse
    """
    df = load_csv(file_path)

    total_records = count_total(df)
    unique_ids = count_unique(df, key_column)
    duplicate_ids = count_duplicates(df, key_column)
    null_counts = count_nulls(df)

    distribution_results = {}

    # Toon alleen distributies voor kolommen die echt bestaan in de dataset.
    for column in distribution_columns:
        if column in df.columns:
            distribution_results[column] = count_per_value(df, column)

    return {
        "file_path": file_path,
        "dataframe": df,
        "total_records": total_records,
        "unique_ids": unique_ids,
        "duplicate_ids": duplicate_ids,
        "null_counts": null_counts,
        "distribution_results": distribution_results,
    }
