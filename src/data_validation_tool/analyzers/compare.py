import pandas as pd


def compare_ids(source_df: pd.DataFrame, target_df: pd.DataFrame, key_column: str) -> dict:
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