#!/usr/bin/env python3
import sys
import pandas as pd
import csv


def main():
    if len(sys.argv) != 3:
        print("Usage: python prepare-threats.py <input.csv> <output.csv>")
        sys.exit(1)

    # Expect the expanded document created by prepare-data script as the input
    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    df = pd.read_csv(input_file)

    # --- Validate required columns ---
    required_cols = ["docID", "Threat", "Study focus", "Study_year"]
    df = df[required_cols]
    df = df.drop_duplicates()

    # --- Save output ---
    df.to_csv(output_file, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
    print(f"Done! Wrote {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()
