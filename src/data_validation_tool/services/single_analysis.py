# from data_validation_tool.analyzers.counts import (
#     count_duplicates,
#     count_nulls,
#     count_per_value,
#     count_total,
#     count_unique,
# )
# from data_validation_tool.loaders.file_loader import load_file


# def run_single_analysis(
#     file_path: str,
#     key_column: str,
#     distribution_columns: list[str],
# ) -> dict:
#     """
#     Voert een single dataset analyse uit op één bestand.

#     Ondersteunde bestandstypen:
#     - CSV
#     - Excel (.xlsx)
#     - JSON

#     Parameters:
#     - file_path: pad naar het inputbestand
#     - key_column: kolom die gebruikt wordt als unieke sleutel
#     - distribution_columns: kolommen waarvan een waardeverdeling getoond moet worden

#     Returns:
#     - dict met alle resultaten van de single analyse
#     """
#     df = load_file(file_path)

#     total_records = count_total(df)
#     unique_ids = count_unique(df, key_column)
#     duplicate_ids = count_duplicates(df, key_column)
#     null_counts = count_nulls(df)

#     distribution_results = {}

#     # Toon alleen distributies voor kolommen die echt bestaan in de dataset.
#     for column in distribution_columns:
#         if column in df.columns:
#             distribution_results[column] = count_per_value(df, column)

#     return {
#         "file_path": file_path,
#         "dataframe": df,
#         "total_records": total_records,
#         "unique_ids": unique_ids,
#         "duplicate_ids": duplicate_ids,
#         "null_counts": null_counts,
#         "distribution_results": distribution_results,
#     }

from data_validation_tool.analyzers.counts import (
    count_duplicates,
    count_nulls,
    count_per_value,
    count_total,
    count_unique,
)
from data_validation_tool.analyzers.single_validations import (
    find_business_duplicates,
    find_missing_required_fields,
    validate_allowed_values,
    validate_fields,
)
from data_validation_tool.loaders.file_loader import load_file


def run_single_analysis(
    file_path: str,
    key_column: str,
    distribution_columns: list[str],
    business_key_columns: list[str] | None = None,
    required_fields: list[str] | None = None,
    field_validations: dict | None = None,
    allowed_values: dict | None = None,
) -> dict:
    """
    Voert een single dataset analyse uit op één bestand.

    Ondersteunde bestandstypen:
    - CSV
    - Excel (.xlsx)
    - JSON

    Parameters:
    - file_path: pad naar het inputbestand
    - key_column: kolom die gebruikt wordt als unieke sleutel
    - distribution_columns: kolommen waarvan een waardeverdeling getoond moet worden
    - business_key_columns: kolommen voor functionele duplicate-detectie
    - required_fields: velden die per record verplicht zijn
    - field_validations: validatieregels per veld, bijvoorbeeld email/telefoon
    - allowed_values: toegestane waarden per veld

    Returns:
    - dict met alle resultaten van de single analyse
    """
    df = load_file(file_path)

    total_records = count_total(df)
    unique_ids = count_unique(df, key_column)
    duplicate_ids = count_duplicates(df, key_column)
    null_counts = count_nulls(df)

    distribution_results = {}

    # Toon alleen distributies voor kolommen die echt bestaan in de dataset.
    for column in distribution_columns:
        if column in df.columns:
            distribution_results[column] = count_per_value(df, column)

    business_duplicates = find_business_duplicates(
        df, key_column, business_key_columns
    )
    missing_required_fields = find_missing_required_fields(
        df, key_column, required_fields
    )
    field_validation_issues = validate_fields(
        df, key_column, field_validations
    )
    allowed_value_issues = validate_allowed_values(
        df, key_column, allowed_values
    )

    return {
        "file_path": file_path,
        "dataframe": df,
        "total_records": total_records,
        "unique_ids": unique_ids,
        "duplicate_ids": duplicate_ids,
        "null_counts": null_counts,
        "distribution_results": distribution_results,
        "business_duplicates": business_duplicates,
        "missing_required_fields": missing_required_fields,
        "field_validation_issues": field_validation_issues,
        "allowed_value_issues": allowed_value_issues,
    }
