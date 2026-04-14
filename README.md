# Data Validation Tool

## Overzicht

Deze tool is ontwikkeld om datasets te analyseren en te vergelijken in het kader van datamigraties. De focus ligt op het snel inzichtelijk maken van verschillen, datakwaliteit en verdelingen tussen bron- en doeldata.

De tool ondersteunt meerdere bestandsformaten en kan gebruikt worden voor zowel:

* analyse van één dataset (profiling)
* vergelijking tussen bron- en doeldata

De huidige versie is een **Minimum Viable Product (MVP)** en is gericht op praktische toepasbaarheid binnen migratieprojecten.

---

## Functionaliteiten

### 1. Single dataset analyse

Analyse van één dataset met de volgende inzichten:

* totaal aantal records
* aantal unieke keys
* aantal duplicate keys
* null-waardes per kolom
* verdeling van geselecteerde kolommen (bijv. status, land)

---

### 2. Vergelijking bron vs doel

Vergelijkt twee datasets op basis van een key en geeft:

* aantal records in bron en doel
* overlap tussen datasets
* records die alleen in bron of doel voorkomen
* distributieverschillen per kolom
* veldverschillen op recordniveau

---

### 3. Ondersteunde bestandsformaten

De tool kan automatisch bestanden inlezen op basis van extensie:

* CSV (`.csv`)
* Excel (`.xlsx`)
* JSON (`.json`)

---

### 4. Export

Resultaten worden geëxporteerd naar:

* CSV-bestanden:

  * `summary.csv`
  * `distribution_differences.csv`
  * `field_differences.csv`

* Excel rapport:

  * `report.xlsx` met meerdere tabbladen

---

## Projectstructuur

```text
src/data_validation_tool/
├── analyzers/        # Data-analyse logica (counts, compare)
├── loaders/          # Inlezen van CSV, Excel en JSON
├── services/         # Orchestratie van analyses
├── reporting/        # Console output en summary builders
├── utils/            # Export en helper functies
├── config.py         # Configuratie
├── main.py           # Entry point
```

---

## Configuratie

Configuratie gebeurt via `config.py`.

Voorbeeld:

```python
SINGLE_FILE_PATH = "data/single/example.csv"
SOURCE_FILE_PATH = "data/compare/bron.json"
TARGET_FILE_PATH = "data/compare/doel.xlsx"

KEY_COLUMN = "id"
DISTRIBUTION_COLUMNS = ["status", "land"]

MODE = "all"  # "single", "compare", "all"
```

---

## Gebruik

Run de tool via:

```bash
make all
```

Of direct:

```bash
PYTHONPATH=src python -m data_validation_tool.main
```

---

## Modi

De tool ondersteunt drie modi:

* `single`
  Alleen analyse van één dataset

* `compare`
  Alleen vergelijking tussen bron en doel

* `all`
  Beide analyses

---

## Huidige beperkingen

Deze versie gaat uit van:

* gelijke kolomnamen tussen bron en doel
* één key-kolom voor matching
* eenvoudige JSON-structuren (platte lijsten)

Complexere migraties (zoals veldmapping, business keys en transformaties) worden nog niet ondersteund.

---

## Toekomstige uitbreidingen

Mogelijke vervolgstappen:

* ondersteuning voor business key matching (i.p.v. technische ID)
* veldmapping tussen bron en doel
* waarde- en fase-mapping
* betere ondersteuning voor geneste JSON
* uitbreiding van validatieregels
* geautomatiseerde tests

---

## Doel

De tool is bedoeld als:

* hulpmiddel voor datakwaliteitsanalyse
* ondersteuning bij migratievalidatie
* snelle "health check" van datasets

---

## Status

MVP — actief in ontwikkeling