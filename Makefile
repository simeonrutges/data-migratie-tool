# Markeer targets als "phony" (geen echte bestanden)
# Dit voorkomt issues als er toevallig een bestand bestaat met dezelfde naam
.PHONY: run format install open all

# --------------------------------------------------
# Run de applicatie
# --------------------------------------------------
# - Zorgt dat de output map bestaat
# - Zet PYTHONPATH zodat Python de src/ map herkent
# - Start de main module
run:
	mkdir -p output
	PYTHONPATH=src uv run python -m data_validation_tool.main


# --------------------------------------------------
# Format de code met Black
# --------------------------------------------------
# - Zorgt voor consistente code formatting
# - Handig om vóór commit te draaien
format:
	uv run black .


# --------------------------------------------------
# Installeer dependencies
# --------------------------------------------------
# - Synchroniseert je virtual environment met pyproject.toml
# - Gebruik dit bij eerste setup of na dependency wijzigingen
install:
	uv sync


# --------------------------------------------------
# Open het gegenereerde Excel rapport
# --------------------------------------------------
# - Alleen voor macOS (gebruikt 'open' command)
# - Opent output/report.xlsx in Excel of default app
open:
	open output/report.xlsx


# --------------------------------------------------
# Alles in één keer uitvoeren
# --------------------------------------------------
# - Run de applicatie
# - Open daarna automatisch het Excel rapport
# - Ideaal voor snelle workflow
# - werkt alleen op macOS
all: run open