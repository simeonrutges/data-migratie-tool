# Data Validation Tool

## Overview

This project provides a lightweight data validation tool designed to compare datasets and identify inconsistencies. It is particularly useful in data migration scenarios, where data from a source system must be validated against a target system.

The tool performs automated checks on CSV-based datasets and generates both console output and structured reports (CSV and Excel).

---

## Features

### Single Dataset Analysis

* Total number of records
* Unique and duplicate ID detection
* Null value analysis per column
* Value distribution (e.g. status counts)

### Dataset Comparison (Source vs Target)

* Total IDs in source and target
* Matching IDs
* Missing IDs in either dataset
* Row-level field comparison

### Distribution Comparison

* Compares value distributions per column
* Highlights differences between source and target

### Reporting

* Console summary output
* CSV exports:

  * summary.csv
  * distribution_differences.csv
  * field_differences.csv
* Excel report:

  * Multiple sheets (summary, distribution, field differences)
  * Styled headers
  * Auto-sized columns
  * Filters enabled
  * Differences highlighted

---

## Project Structure

```
src/data_validation_tool/
  loaders/       # Data loading logic (e.g. CSV)
  analyzers/     # Core analysis and comparison logic
  utils/         # Helper functions (e.g. export, styling)
  main.py        # Application entry point

output/          # Generated reports (CSV and Excel)
```

---

## Usage

### Run the application

```
make run
```

### Open the Excel report

```
make open
```

### Run and open in one step

```
make all
```

### Format the code

```
make format
```

### Install dependencies

```
make install
```

---

## Input Data

By default, the tool expects:

```
data/single/example.csv
data/compare/bron.csv
data/compare/doel.csv
```

These paths are currently hardcoded in `main.py`.

---

## Output

After running the tool, the following files are generated:

```
output/
  summary.csv
  distribution_differences.csv
  field_differences.csv
  report.xlsx
```

The Excel report contains:

* Summary metrics
* Distribution differences
* Field-level differences

---

## Technologies Used

* Python
* pandas
* openpyxl
* Makefile (for workflow automation)

---

## Notes

* The tool currently supports CSV input.
* The comparison key is hardcoded (default: `id`).
* Output files are not intended to be committed to version control.

---

## Future Improvements

* Configurable input paths and column mappings
* Support for JSON and other formats
* CLI arguments instead of hardcoded paths
* Enhanced validation rules (e.g. tolerances, normalization)
* Improved Excel reporting (conditional formatting, summaries)

---

## License

This project is licensed under the MIT License.