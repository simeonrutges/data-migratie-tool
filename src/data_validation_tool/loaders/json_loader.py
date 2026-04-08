import json
import pandas as pd


def load_json(path: str) -> pd.DataFrame:
    """
    Laadt een JSON-bestand in als pandas DataFrame.

    Ondersteunt:
    - lijst van objecten
    - object met een lijst als top-level waarde

    Parameters:
    - path: pad naar het JSON-bestand

    Returns:
    - pandas DataFrame
    """
    with open(path, "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # Kies de eerste lijst-waarde die we tegenkomen.
        list_value = next(
            (value for value in data.values() if isinstance(value, list)),
            None,
        )

        if list_value is None:
            raise ValueError(
                "JSON-bestand bevat geen lijst met records die omgezet kan worden naar een DataFrame."
            )

        df = pd.DataFrame(list_value)
    else:
        raise ValueError("Niet-ondersteund JSON-formaat.")

    df.columns = [str(column).strip().replace("\ufeff", "") for column in df.columns]

    return df
