# --------------------------------------------------
# Configuratie voor data validation tool
# --------------------------------------------------

# Input bestanden: .json , .csv, .xlsx
# SINGLE_FILE_PATH = "data/single/example.csv"
SINGLE_FILE_PATH = "data/single/example3.json"
SOURCE_FILE_PATH = "data/compare/bron.json"
TARGET_FILE_PATH = "data/compare/doel.xlsx"

# Belangrijke kolommen
KEY_COLUMN = "id"

# Optioneel: kolommen waarvan je een verdeling wilt tonen
# alleen voor de single dataset analyse:
# DISTRIBUTION_COLUMNS = ["status", "land"]
DISTRIBUTION_COLUMNS = ["stats", "lnd", "klnttype"]


# Compare selecteert zelf de belangrijkste distributie kolommen

# Run mode:
# - "single"  -> alleen single dataset analyse
# - "compare" -> alleen bron/doel vergelijking
# - "all"     -> beide
MODE = "single"


# --------------------------------------------------
# Extra configuratie voor uitgebreide single-mode validaties
# --------------------------------------------------

# Functionele duplicate-detectie op business key
BUSINESS_KEY_COLUMNS = ["nm", "stats", "lnd", "klnttype"]

# Velden die verplicht gevuld moeten zijn
REQUIRED_FIELDS = ["nm", "stats", "lnd", "klnttype"]

# Toegestane waarden per veld
ALLOWED_VALUES = {
    "stats": ["Ac", "In"],
}

# # Veldvalidaties
# FIELD_VALIDATIONS = {
#     "email": {
#         "type": "email",
#         "single_value_only": True,
#         "trim_whitespace": True,
#         "normalize_lowercase": True,
#     },
#     "telefoon": {
#         "type": "phone",
#         "single_value_only": True,
#         "trim_whitespace": True,
#     },

# Veldvalidaties
FIELD_VALIDATIONS = {}
