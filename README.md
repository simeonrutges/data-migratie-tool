# Data Validation Tool

Een Python-tool voor het analyseren en valideren van datasets (CSV, JSON, Excel).

## Doel

Deze tool helpt bij:
- data kwaliteit controleren
- migratietesten ondersteunen
- inzicht krijgen in datasets

## Functionaliteit

### Single dataset analyse
- totaal aantal records
- null/lege waarden per kolom
- unieke waarden
- duplicate detectie
- verdeling per kolom (bijv. status)

### Dataset vergelijking (WIP)
- bron vs doel vergelijking
- ontbrekende records
- extra records
- veldverschillen

## Tech stack

- Python
- pandas
- uv

## Setup

```bash
git clone <repo-url>
cd data-validation-tool
uv sync