#!/usr/bin/env python3
import sys
import pandas as pd
import requests
import time
import rapidfuzz.fuzz as fuzz

#
# == Script to process results from prepare-data script, and look for document urls
# == Saves the output for manual update of long, lat columns
#

SLEEP_BETWEEN_REQUESTS = 1
N_COLUMNS = 6  # Number of columns to keep from input

def get_crossref_doi(author, title):
    """Query Crossref for DOI link using author and title."""
    base_url = "https://api.crossref.org/works"
    params = {
        "query.author": author,
        "query.title": title,
        "rows": 5
    }
    try:
        r = requests.get(base_url, params=params, timeout=30)
        r.raise_for_status()
        items = r.json().get("message", {}).get("items", [])
        print(f"Looking for: {title}")
        for it in items:
            candidate_title = " ".join(it.get("title", []))    
            if fuzz.ratio(candidate_title.lower(), title.lower()) >= 90:  # 0–100 scale
                print(f"Found: {candidate_title}")
                return f"https://doi.org/{it['DOI']}"
        return None
    except Exception as e:
        print(f"Error fetching DOI for '{title}': {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python retrieve-documents.py <input.xlsx|.csv> <output.xlsx>")
        sys.exit(1)

# - expect the expanded document created by prepare-data script as the input
    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    # --- Read input ---
    df = pd.read_csv(input_file)

    # --- Keep only first N columns ---
    df = df.iloc[:, :N_COLUMNS]

    # --- Drop duplicates based on the first column only ---
    df = df.drop_duplicates(subset=df.columns[0], keep='first').reset_index(drop=True)

    # --- Validate required columns ---
    required_cols = {"Authors", "Document title"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Input file must have 'Authors' and 'Document title' columns")

    # --- Query Crossref for each row ---
    urls = []
    for _, row in df.iterrows():
        authors = row["Authors"]
        title   = row["Document title"]

        if pd.isna(authors) or pd.isna(title):
            urls.append("Not found")
            continue

        url = get_crossref_doi(authors, title)
        urls.append(url if url else "Not found")
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    df['URL'] = urls

    # --- Save output ---
    df.to_excel(output_file, index=False)
    print(f"Done! Wrote {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()
