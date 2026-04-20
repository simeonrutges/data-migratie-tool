import pandas as pd


def count_total(df: pd.DataFrame) -> int:
    """Geef het totaal aantal records terug."""
    return len(df)


def count_nulls(df: pd.DataFrame) -> pd.Series:
    """Geef per kolom het aantal null/lege waarden terug."""
    return df.isnull().sum()


def count_unique(df: pd.DataFrame, column: str) -> int:
    """Geef het aantal unieke waarden in een kolom terug."""
    return df[column].nunique()


def count_duplicates(df: pd.DataFrame, column: str) -> int:
    """Geef het aantal duplicate records terug op basis van een kolom."""
    return df.duplicated(subset=[column]).sum()


def count_per_value(df: pd.DataFrame, column: str) -> pd.Series:
    """Geef het aantal records per waarde in een kolom terug."""
    return df[column].value_counts(dropna=False)


def get_duplicate_details(df, column: str) -> list[dict]:
    value_counts = df[column].value_counts(dropna=False)
    duplicate_counts = value_counts[value_counts > 1]

    return [
        {"value": value, "count": int(count)}
        for value, count in duplicate_counts.items()
    ]
