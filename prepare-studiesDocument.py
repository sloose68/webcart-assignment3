#!/usr/bin/env python3
import sys
import pandas as pd

# === Pepares the studiesDocument  document metadata by trimming columns before 'long' ===

if len(sys.argv) != 3:
    print("Usage: python prepare-studiesDocument.py <input.xls> <output.csv>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

# Read your spreadsheet
df = pd.read_excel(input_file)

# Replace line breaks (\n and \r) with '; ' in all string cells
df = df.applymap(
    lambda x: x.replace('\n', '; ').replace('\r', '; ') if isinstance(x, str) else x
)


# Find the index of the first column named 'long'
try:
    long_index = df.columns.get_loc('Long')
except KeyError:
    print("Error: Column 'long' not found in input file.")
    sys.exit(1)

# Slice all columns up to (but not including) 'long'
df_trimmed = df.iloc[:, :long_index]

# Save the trimmed output
df_trimmed.to_csv(output_file, index=False)
print(f"Done! Wrote {len(df_trimmed)} rows to {output_file}")
