import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """
    Laadt een CSV-bestand in als pandas DataFrame.

    Ondersteunt automatisch komma- en puntkomma-gescheiden CSV's.
    Maakt kolomnamen schoon zodat verborgen tekens, BOM en spaties
    geen problemen geven bij hardcoded kolomnamen zoals 'id'.
    """
    df = pd.read_csv(
        path,
        sep=None,
        engine="python",
        encoding="utf-8-sig",
        na_values=["", " ", "NULL", "null", "N/A"],
    )

    # Maak kolomnamen schoon:
    # - verwijder spaties aan begin/eind
    # - verwijder BOM als die in de eerste kolomnaam zit
    df.columns = [str(column).strip().replace("\ufeff", "") for column in df.columns]

    return df
