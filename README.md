# Web Cartography Assignment 3 – Python Tools (webcart-assignment3)

**Author:** Stuart Loose

This repository contains a collection of **Python scripts and supporting tools** developed for **Assignment 3** of the **Web Cartography** course at UniSA.

The main purpose of these tools is to **process and transform source spreadsheets** into **clean, distinct CSV files** suitable for import as tables or feature layers in **ArcGIS Pro**.

## Features

* **Data transformation**: Clean and normalise raw spreadsheet data for GIS import.
* **DOI lookup**: Automatically find source document DOIs using Crossref.
* **Ecosystem classification**: Map class codes to standard high-level ecosystem categories.

## Usage

Each script has specific functionality, typically accepting **input and output filenames** as command-line arguments. For example:

```bash
python prepare-docs.py source.xlsx output.csv
```

## Requirements

* Python 3.10+
* Packages:

  * `pandas`
  * `requests`
  * `openpyxl` (for Excel support)
  * `rapidfuzz` (for fuzzy matching of document titles)
