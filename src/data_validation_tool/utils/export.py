import pandas as pd


def export_differences_to_csv(differences: list[dict], output_path: str) -> None:
    """
    Exporteert veldverschillen naar een CSV-bestand.

    Parameters:
    - differences: lijst met verschillen (dicts met keys: id, kolom, bron, doel)
    - output_path: pad naar het outputbestand (bijv. 'output/field_differences.csv')

    Werking:
    - Zet de lijst om naar een pandas DataFrame
    - Schrijft deze weg naar CSV
    """

    # Als er geen verschillen zijn, maken we alsnog een lege file met kolomnamen
    if not differences:
        df = pd.DataFrame(columns=["id", "kolom", "bron", "doel"])
    else:
        df = pd.DataFrame(differences)

    # Schrijf naar CSV (zonder index kolom)
    df.to_csv(output_path, index=False)