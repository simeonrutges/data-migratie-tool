def validate_required_column(columns, required_column: str, dataset_name: str) -> None:
    """
    Controleert of een verplichte kolom aanwezig is in een dataset.

    Parameters:
    - columns: lijst of index met kolomnamen
    - required_column: kolom die verplicht aanwezig moet zijn
    - dataset_name: naam van de dataset voor een duidelijke foutmelding

    Raises:
    - ValueError: als de verplichte kolom ontbreekt
    """
    if required_column not in columns:
        available_columns = ", ".join(str(column) for column in columns)
        raise ValueError(
            f"Verplichte kolom '{required_column}' ontbreekt in dataset "
            f"'{dataset_name}'. Beschikbare kolommen: {available_columns}"
        )
