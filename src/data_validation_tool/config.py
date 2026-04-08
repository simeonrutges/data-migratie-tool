# --------------------------------------------------
# Configuratie voor data validation tool
# --------------------------------------------------

# Input bestanden: .json , .csv, .xlsx
SINGLE_FILE_PATH = "data/single/example.csv"
SOURCE_FILE_PATH = "data/compare/bron.json"
TARGET_FILE_PATH = "data/compare/doel.xlsx"

# Belangrijke kolommen
KEY_COLUMN = "id"

# Optioneel: kolommen waarvan je een verdeling wilt tonen
# alleen voor de single dataset analyse:
DISTRIBUTION_COLUMNS = ["status", "land"]

# Compare selecteert zelf de belangrijkste distributie kolommen

# Run mode:
# - "single"  -> alleen single dataset analyse
# - "compare" -> alleen bron/doel vergelijking
# - "all"     -> beide
MODE = "compare"
