# Data Validation Tool

Een Python-tool voor het analyseren en vergelijken van datasets (CSV).

De tool helpt bij:
- data-analyse (aantallen, nulls, duplicaten)
- vergelijking tussen bron- en doeldatasets
- detecteren van verschillen per record en per kolom
- inzicht in distributies (bijv. statusverdeling)

---

## Functionaliteiten

### Single dataset analyse
- totaal aantal records
- aantal unieke IDs
- duplicate IDs
- nulls per kolom
- verdeling per kolom (bijv. status)

---

### Vergelijking (bron vs doel)
- aantal IDs in bron en doel
- overlap tussen datasets
- ontbrekende records (alleen in bron / alleen in doel)

---

### Distributie vergelijking
Vergelijkt hoe waarden verdeeld zijn.

Voorbeeld:

status:
Actief +2
Inactief -2


---

### Field-level vergelijking
Toont exacte verschillen per record:

ID 9 - status: Inactief -> Actief

---

### Lichte normalisatie
Bij vergelijking wordt rekening gehouden met:
- hoofdletters (case-insensitive)
- spaties (trim)

Voorbeeld:

" Actief " == "actief"


Accenten worden **niet genegeerd**:


"García" != "Garcia"


---

## Projectstructuur

src/
data_validation_tool/
analyzers/
loaders/
utils/
main.py
data/
single/
compare/
Makefile

---

## Runnen

Gebruik Makefile:

```bash
make run

Of direct:

PYTHONPATH=src uv run python -m data_validation_tool.main
Vereisten
Python 3.13+
uv (package manager)

Installeren:

uv sync
Toekomstige uitbreidingen
ondersteuning voor JSON en Excel
export naar CSV/Excel
configureerbare kolommen en keys
verbeterde output/rapportage

---

# Wat nu doen

1. Open `README.md`  
2. Plak dit erin  
3. Save  

Daarna:

```bash
git add README.md
git commit -m "Add README with project overview"
git push