import pandas as pd


def compare_ids(
    source_df: pd.DataFrame, target_df: pd.DataFrame, key_column: str
) -> dict:
    source_ids = set(source_df[key_column].dropna())
    target_ids = set(target_df[key_column].dropna())

    only_in_source = source_ids - target_ids
    only_in_target = target_ids - source_ids
    in_both = source_ids & target_ids

    return {
        "only_in_source": sorted(only_in_source),
        "only_in_target": sorted(only_in_target),
        "in_both_count": len(in_both),
    }


def compare_distribution(source_df: pd.DataFrame, target_df: pd.DataFrame, column: str):
    source_counts = source_df[column].value_counts(dropna=False)
    target_counts = target_df[column].value_counts(dropna=False)

    # Combineer beide indexen (alle unieke waarden)
    all_values = set(source_counts.index).union(set(target_counts.index))

    differences = {}

    for value in all_values:
        source_val = source_counts.get(value, 0)
        target_val = target_counts.get(value, 0)

        differences[value] = target_val - source_val

    return source_counts, target_counts, differences


def get_interesting_columns(
    df: pd.DataFrame,
    max_unique: int = 10,
    exclude_columns: list[str] | None = None,
) -> list[str]:
    if exclude_columns is None:
        exclude_columns = []

    interesting_columns = []

    for column in df.columns:
        if column in exclude_columns:
            continue

        if "datum" in column.lower() or "date" in column.lower():
            continue

        unique_count = df[column].nunique(dropna=False)
        row_count = len(df)

        if unique_count <= max_unique and unique_count < row_count:
            interesting_columns.append(column)

    return interesting_columns


def normalize_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, str):
        return value.strip().lower()

    return value


def compare_rows(
    source_df: pd.DataFrame,
    target_df: pd.DataFrame,
    key_column: str,
) -> list[dict]:
    merged_df = source_df.merge(
        target_df,
        on=key_column,
        how="inner",
        suffixes=("_bron", "_doel"),
    )

    differences = []

    for _, row in merged_df.iterrows():
        for column in source_df.columns:
            if column == key_column:
                continue

            source_value = row[f"{column}_bron"]
            target_value = row[f"{column}_doel"]

            normalized_source = normalize_value(source_value)
            normalized_target = normalize_value(target_value)

            if normalized_source == normalized_target:
                continue

            differences.append(
                {
                    "key": row[key_column],
                    "kolom": column,
                    "bron": source_value,
                    "doel": target_value,
                }
            )

    return differences
