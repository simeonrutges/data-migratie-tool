from pathlib import Path

import pandas as pd

from data_validation_tool.loaders.csv_loader import load_csv
from data_validation_tool.loaders.excel_loader import load_excel
from data_validation_tool.loaders.json_loader import load_json


def load_file(path: str) -> pd.DataFrame:
    """
    Laadt een bestand in op basis van extensie.

    Ondersteunde types:
    - .csv
    - .xlsx
    - .json
    """
    suffix = Path(path).suffix.lower()

    if suffix == ".csv":
        return load_csv(path)

    if suffix == ".xlsx":
        return load_excel(path)

    if suffix == ".json":
        return load_json(path)

    raise ValueError(
        f"Niet-ondersteund bestandstype: '{suffix}'. Gebruik .csv, .xlsx of .json."
    )
