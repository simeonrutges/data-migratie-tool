import pandas as pd


def export_differences_to_csv(differences: list[dict], output_path: str) -> None:
    """
    Exporteert veldverschillen naar een CSV-bestand.

    Parameters:
    - differences: lijst met verschillen (dicts met keys: id, kolom, bron, doel)
    - output_path: pad naar het outputbestand
    """
    if not differences:
        df = pd.DataFrame(columns=["id", "kolom", "bron", "doel"])
    else:
        df = pd.DataFrame(differences)

    df.to_csv(output_path, index=False)


def export_summary_to_csv(summary_data: list[dict], output_path: str) -> None:
    """
    Exporteert samenvattingsgegevens naar een CSV-bestand.

    Parameters:
    - summary_data: lijst met samenvattingsregels
    - output_path: pad naar het outputbestand
    """
    df = pd.DataFrame(summary_data)
    df.to_csv(output_path, index=False)


def export_distribution_to_csv(distribution_data: list[dict], output_path: str) -> None:
    """
    Exporteert distributieverschillen naar een CSV-bestand.

    Parameters:
    - distribution_data: lijst met distributieverschillen per kolom/waarde
    - output_path: pad naar het outputbestand
    """
    df = pd.DataFrame(distribution_data)
    df.to_csv(output_path, index=False)
