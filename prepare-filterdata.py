#!/usr/bin/env python3
import sys
import pandas as pd
import os

#
# === Script to generate a filterdata table containing expanded document data - Basically
# === The data from prepare-data; It also adds the ecosystem categories (copy of the ecosystems logic)
# === It also takes the processed file that co-ordinates and spatial information added, to include these coluumns 
def combine_codes(sub):
    return "; ".join(
        f"{c}, {e}"
        for c, e in zip(sub["Class code"], sub["Explicit or Inferred"])
    )

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python prepare-filterdata.py <input.csv> <lookup.xlsx> <output.csv> [spatialdoc.xls]")
        sys.exit(1)

    input_file      = sys.argv[1]
    lookup_file     = sys.argv[2]
    output_file     = sys.argv[3]
    spatialdoc_file = sys.argv[4] if len(sys.argv) == 5 else None

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

    # --- Optional merge with spatialdoc_file ---
    if spatialdoc_file and os.path.exists(spatialdoc_file):
        df_spatial = pd.read_excel(spatialdoc_file)

        # Replace line breaks (\n and \r) with '; ' in all string cells
        df_spatial = df_spatial.applymap(
            lambda x: x.replace('\n', '; ').replace('\r', '; ') if isinstance(x, str) else x
        )
        df = df.merge(df_spatial[["docID", "URL", "spatial details", "polygon details"]], on="docID", how="left")

    # --- Save output ---
    df.to_csv(output_file, index=False)
    print(f"Done! Wrote {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()