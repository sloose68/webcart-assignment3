import sys
import pandas as pd

if len(sys.argv) != 3:
    print("Usage: python prepare-docs-dedup.py <input.xlsx> <output.xlsx>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

# Read your spreadsheet
df = pd.read_excel(input_file,header=0, skiprows=1)  # or pd.read_csv("input.csv")

# remove any trailing spaces
df.columns = df.columns.str.strip()

# --- Fill blanks with the last non-blank value above ---
df = df.ffill()

# add in docId column
df['docID'] = df.groupby(['Authors','Document title','Year']).ngroup() + 1

# Move 'docID' to the front
cols = ['docID'] + [c for c in df.columns if c != 'docID']
df = df[cols]

# --- Remove duplicate rows ---
df = df.drop_duplicates()

# Next add simplified ecosystem category from lookup spreadsheet


# --- Save the result ---
df.to_csv(output_file, index=False)
