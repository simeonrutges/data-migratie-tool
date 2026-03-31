def print_single_summary(
    file_path: str,
    key_column: str,
    total_records: int,
    unique_ids: int,
    duplicate_ids: int,
    null_counts,
) -> None:
    """
    Print een samenvatting van de single dataset analyse.
    """
    print("\nSingle dataset:")
    print(f"- bestand: {file_path}")
    print(f"- records: {total_records}")
    print(f"- unieke {key_column}s: {unique_ids}")
    print(f"- duplicate {key_column}s: {duplicate_ids}")

    non_zero_nulls = null_counts[null_counts > 0]
    if non_zero_nulls.empty:
        print("- nulls: geen")
    else:
        null_summary = ", ".join(
            f"{column}={count}" for column, count in non_zero_nulls.items()
        )
        print(f"- nulls: {null_summary}")


def print_compare_summary(
    source_file_path: str,
    target_file_path: str,
    key_column: str,
    source_ids,
    target_ids,
    compare_result: dict,
) -> None:
    """
    Print een samenvatting van de vergelijking tussen bron en doel.
    """
    print("\nVergelijking bron vs doel:")
    print(f"- bronbestand: {source_file_path}")
    print(f"- doelbestand: {target_file_path}")
    print(f"- bron {key_column}s: {len(source_ids)}")
    print(f"- doel {key_column}s: {len(target_ids)}")
    print(f"- overeenkomende {key_column}s: {compare_result['in_both_count']}")
    print(f"- alleen in bron: {compare_result['only_in_source']}")
    print(f"- alleen in doel: {compare_result['only_in_target']}")


def print_distribution_differences(distribution_export: list[dict]) -> None:
    """
    Print distributieverschillen gegroepeerd per kolom.
    """
    print("\nDistributieverschillen:")

    if distribution_export:
        distribution_by_column = {}

        for item in distribution_export:
            column = item["kolom"]
            value = item["waarde"]
            difference = item["verschil_doel_min_bron"]

            if column not in distribution_by_column:
                distribution_by_column[column] = []

            distribution_by_column[column].append(f"{value} {difference:+}")

        for column, differences in distribution_by_column.items():
            diff_summary = ", ".join(differences)
            print(f"- {column}: {diff_summary}")
    else:
        print("- geen distributieverschillen gevonden")


def print_row_differences(row_differences: list[dict], key_column: str) -> None:
    """
    Print veldverschillen per record.
    """
    print("\nVeldverschillen:")

    if not row_differences:
        print("- geen veldverschillen gevonden")
    else:
        print(f"- {len(row_differences)} verschil(len) gevonden")
        for diff in row_differences:
            print(
                f"  - {key_column} {diff['key']} | {diff['kolom']} | "
                f"{diff['bron']} -> {diff['doel']}"
            )


def print_single_distributions(distribution_results: dict) -> None:
    """
    Print de geconfigureerde verdelingen voor de single dataset.
    """
    print("\nDetails single dataset:")

    if distribution_results:
        for column, counts in distribution_results.items():
            print(f"\nVerdeling van {column}:")
            for value, count in counts.items():
                label = "Leeg" if str(value) == "nan" else value
                print(f"- {label}: {count}")
    else:
        print("- Geen distributiekolommen geconfigureerd of gevonden")
