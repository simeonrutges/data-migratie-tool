import pandas as pd


def load_excel(path: str, sheet_name: int | str = 0) -> pd.DataFrame:
    """
    Laadt een Excel-bestand in als pandas DataFrame.

    Parameters:
    - path: pad naar het Excel-bestand
    - sheet_name: sheet index of naam, standaard eerste sheet

    Returns:
    - pandas DataFrame
    """
    df = pd.read_excel(path, sheet_name=sheet_name)

    # Maak kolomnamen schoon voor consistente verwerking.
    df.columns = [str(column).strip().replace("\ufeff", "") for column in df.columns]

    return df
