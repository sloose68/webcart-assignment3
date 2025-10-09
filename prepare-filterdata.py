#!/usr/bin/env python3
import sys
import pandas as pd

#
# === Script to generate a table that can be used for filtering.
# === Basically, the flattenned file, but with the simplified ecosystem groups

# function to join ecosystem class codes, and explict / inferred to simplify rows, but not lose data
def combine_codes(sub):
    return "; ".join(
        f"{c}, {e}"
        for c, e in zip(sub["Class code"], sub["Explicit or Inferred"])
    )


def main():
    if len(sys.argv) != 4:
        print("Usage: python prepare-ecosystems.py <input.csv> <lookup.xlsx> <output.csv>")
        sys.exit(1)

    # Expect the expanded document created by prepare-data script as the input
    input_file  = sys.argv[1]
    lookup_file = sys.argv[2]
    output_file = sys.argv[3]

    df = pd.read_csv(input_file)

    # --- Validate required columns ---

    df_excel = pd.read_excel(lookup_file, sheet_name="CICES V5.1", header=4)

    # Strip whitespace from column names just in case
    df_excel.columns = df_excel.columns.str.strip()

    # Create lookup dictionary
    lookup_dict = pd.Series(df_excel["Section"].values,
                            index=df_excel["Code"]).to_dict()

    # Map class code to simplified ecosystem category and strip parentheses
    df["Ecosystem_Category"] = df["Class code"].map(lookup_dict)
    df["Ecosystem_Category"] = df["Ecosystem_Category"].str.replace(
        r"\s*\(.*?\)", "", regex=True
    )

    # Now de-dup using all fields except the detailed class code and exp/inf fields
    exclude_cols = ['Class code', 'Explicit or Inferred']
    groupby_cols = [col for col in df.columns if col not in exclude_cols]

    # Group by everything else, and combine the excluded columns as strings
    df = (
        df.groupby(groupby_cols, as_index=False)
        .apply(
            lambda g: pd.Series({
                "Class code": combine_codes(g)
            }),
            include_groups=False   # <-- this silences the warning
        )
        .reset_index()  # bring group keys back as columns
    )

    # --- Save output ---
    df.to_csv(output_file, index=False)
    print(f"Done! Wrote {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()
