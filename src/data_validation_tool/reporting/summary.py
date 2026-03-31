def build_summary_export(
    single_file_path: str,
    source_file_path: str,
    target_file_path: str,
    key_column: str,
    total_records: int,
    unique_ids: int,
    duplicate_ids: int,
    source_ids,
    target_ids,
    compare_result: dict,
    row_differences: list[dict],
) -> list[dict]:
    """
    Bouwt de samenvattingsdata voor export naar CSV/Excel.

    Returns:
    - lijst van dicts geschikt voor export
    """
    return [
        {"categorie": "single_dataset", "metric": "bestand", "value": single_file_path},
        {"categorie": "single_dataset", "metric": "records", "value": total_records},
        {
            "categorie": "single_dataset",
            "metric": f"unieke_{key_column}s",
            "value": unique_ids,
        },
        {
            "categorie": "single_dataset",
            "metric": f"duplicate_{key_column}s",
            "value": duplicate_ids,
        },
        {"categorie": "compare", "metric": "bronbestand", "value": source_file_path},
        {"categorie": "compare", "metric": "doelbestand", "value": target_file_path},
        {
            "categorie": "compare",
            "metric": f"bron_{key_column}s",
            "value": len(source_ids),
        },
        {
            "categorie": "compare",
            "metric": f"doel_{key_column}s",
            "value": len(target_ids),
        },
        {
            "categorie": "compare",
            "metric": f"overeenkomende_{key_column}s",
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
