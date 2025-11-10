#!/usr/bin/env python3
import sys
import pandas as pd
import csv

###
# Script to prepare ecosystems csv file.
# Uses the result of prepared-data script
###

# Function to join ecosystem class codes and explicit/inferred labels
def combine_codes(sub):
    return "; ".join(
        f"{c}, {e}"
        for c, e in zip(sub["Class code"], sub["Explicit or Inferred"])
    )

def main():
    if len(sys.argv) != 4:
        print("Usage: python prepare-ecosystems.py <input.csv> <lookup.xlsx> <output.csv>")
        sys.exit(1)

    input_file  = sys.argv[1]
    lookup_file = sys.argv[2]
    output_file = sys.argv[3]
    
    df = pd.read_csv(input_file)

    # --- Validate required columns ---
    required_cols = ["docID", "Class code", "Explicit or Inferred", "Study focus", "Study_year"]
    df = df[required_cols]

    df_excel = pd.read_excel(lookup_file, sheet_name="CICES V5.1", header=4)
    df_excel.columns = df_excel.columns.str.strip()

    # Create lookup dictionary
    lookup_dict = pd.Series(df_excel["Section"].values,
                            index=df_excel["Code"]).to_dict()

    # Map class code to simplified ecosystem category and strip parentheses
    df["Ecosystem_Category"] = df["Class code"].map(lookup_dict)
    df["Ecosystem_Category"] = df["Ecosystem_Category"].str.replace(
        r"\s*\(.*?\)", "", regex=True
    )

    # Group by docID and Ecosystem_Category
    dup_cols = ["docID", "Ecosystem_Category"]
    df = (
        df.groupby(dup_cols, as_index=False)
          .apply(lambda g: pd.Series({
              "Class code": combine_codes(g),
              "Study_year": g["Study_year"].iloc[0],
              "Study focus": g["Study focus"].iloc[0]
          }))
          .reset_index(drop=True)
    )

    # --- Save output ---
    df.to_csv(output_file, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
    print(f"Done! Wrote {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()
