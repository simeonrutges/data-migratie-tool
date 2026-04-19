import re
import pandas as pd

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_ALLOWED_REGEX = re.compile(r"^[\d\s\-\+\(\)]+$")


def is_missing_value(value):
    """Check of een waarde leeg/null is."""
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def normalize_business_value(value):
    """Normaliseer waarde voor duplicate-detectie."""
    if is_missing_value(value):
        return None
    if isinstance(value, str):
        return value.strip().lower()
    return value


def split_possible_multi_value(value: str):
    """Splits waarden zoals 'a,b' of 'a/b'."""
    parts = re.split(r"[,;/|]", value)
    return [p.strip() for p in parts if p.strip()]


# --------------------------------------------------
# Business duplicates
# --------------------------------------------------


def find_business_duplicates(df, key_column, business_key_columns):
    """Zoek duplicaten op basis van business key velden."""
    if not business_key_columns:
        return []

    if any(col not in df.columns for col in business_key_columns):
        return []

    temp_df = df.copy()

    norm_cols = []
    for col in business_key_columns:
        norm_col = f"__norm_{col}"
        temp_df[norm_col] = temp_df[col].apply(normalize_business_value)
        norm_cols.append(norm_col)

    temp_df = temp_df.dropna(subset=norm_cols)

    results = []

    for values, group in temp_df.groupby(norm_cols):
        if len(group) <= 1:
            continue

        if not isinstance(values, tuple):
            values = (values,)

        business_key = dict(zip(business_key_columns, values))
        ids = group[key_column].tolist() if key_column in group.columns else []

        results.append(
            {
                "business_key": business_key,
                "count": len(group),
                "ids": ids,
            }
        )

    return results


# --------------------------------------------------
# Required fields
# --------------------------------------------------


def find_missing_required_fields(df, key_column, required_fields):
    """Geef records terug waar verplichte velden ontbreken."""
    if not required_fields:
        return []

    results = []

    for _, row in df.iterrows():
        missing = []

        for field in required_fields:
            if field not in df.columns or is_missing_value(row[field]):
                missing.append(field)

        if missing:
            record_id = row[key_column] if key_column in df.columns else None
            results.append(
                {
                    "id": record_id,
                    "missing_fields": missing,
                }
            )

    return results


# --------------------------------------------------
# Allowed values
# --------------------------------------------------


def validate_allowed_values(df, key_column, allowed_values):
    """Check of waarden binnen toegestane lijst vallen."""
    if not allowed_values:
        return []

    results = []

    for field, allowed in allowed_values.items():
        if field not in df.columns:
            continue

        for _, row in df.iterrows():
            value = row[field]

            if is_missing_value(value):
                continue

            if value not in allowed:
                record_id = row[key_column] if key_column in df.columns else None
                results.append(
                    {
                        "id": record_id,
                        "field": field,
                        "value": value,
                        "allowed_values": allowed,
                    }
                )

    return results


# --------------------------------------------------
# Field validation (email / phone)
# --------------------------------------------------


def validate_email(value, rules):
    if is_missing_value(value):
        return []

    issues = []

    if not isinstance(value, str):
        return ["invalid_format"]

    if rules.get("trim_whitespace") and value != value.strip():
        issues.append("whitespace")

    value = value.strip()

    if rules.get("single_value_only"):
        if len(split_possible_multi_value(value)) > 1:
            return ["multiple_values"]

    if not EMAIL_REGEX.match(value):
        issues.append("invalid_format")

    if rules.get("normalize_lowercase") and value != value.lower():
        issues.append("not_lowercase")

    return issues


def validate_phone(value, rules):
    if is_missing_value(value):
        return []

    issues = []

    if not isinstance(value, str):
        return ["invalid_format"]

    if rules.get("trim_whitespace") and value != value.strip():
        issues.append("whitespace")

    value = value.strip()

    if rules.get("single_value_only"):
        if len(split_possible_multi_value(value)) > 1:
            return ["multiple_values"]

    if not PHONE_ALLOWED_REGEX.match(value):
        return ["invalid_format"]

    digits = re.sub(r"\D", "", value)

    if len(digits) < 8:
        issues.append("too_short")
    elif len(digits) > 15:
        issues.append("too_long")

    return issues


def validate_fields(df, key_column, field_validations):
    """Voer validaties uit op basis van config."""
    if not field_validations:
        return []

    results = []

    for field, rules in field_validations.items():
        if field not in df.columns:
            continue

        for _, row in df.iterrows():
            value = row[field]

            if rules.get("type") == "email":
                issues = validate_email(value, rules)
            elif rules.get("type") == "phone":
                issues = validate_phone(value, rules)
            else:
                continue

            if not issues:
                continue

            record_id = row[key_column] if key_column in df.columns else None

            results.append(
                {
                    "id": record_id,
                    "field": field,
                    "value": value,
                    "issues": issues,
                }
            )

    return results

# Extra: welke duplicate ids


