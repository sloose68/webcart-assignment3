#!/usr/bin/env python3
import sys
import pandas as pd
import os

#
# === Script to generate a filterdata table containing expanded document data
# === The data from prepare-data; It also adds the ecosystem categories (copy of the ecosystems logic)
# 
def combine_codes(sub):
    return "; ".join(
        f"{c}, {e}"
        for c, e in zip(sub["Class code"], sub["Explicit or Inferred"])
    )

def main():
    if len(sys.argv) != 4:
        print("Usage: python prepare-filterdata.py <input.csv> <lookup.xlsx> <output.csv>")
        sys.exit(1)

    input_file      = sys.argv[1]
    lookup_file     = sys.argv[2]
    output_file     = sys.argv[3]

    df = pd.read_csv(input_file)

    # --- Load lookup and map ecosystem categories ---
    df_excel = pd.read_excel(lookup_file, sheet_name="CICES V5.1", header=4)
    df_excel.columns = df_excel.columns.str.strip()
    lookup_dict = pd.Series(df_excel["Section"].values, index=df_excel["Code"]).to_dict()

    df["Ecosystem_Category"] = df["Class code"].map(lookup_dict)
    df["Ecosystem_Category"] = df["Ecosystem_Category"].str.replace(r"\s*\(.*?\)", "", regex=True)

    # --- Group and combine codes ---
    exclude_cols = ['Class code', 'Explicit or Inferred']
    groupby_cols = [col for col in df.columns if col not in exclude_cols]

    df = (
        df.groupby(groupby_cols, as_index=False)
        .apply(lambda g: pd.Series({"Class code": combine_codes(g)}), include_groups=False)
        .reset_index()
    )

    # --- Save output ---
    df.to_csv(output_file, index=False)
    print(f"Done! Wrote {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()