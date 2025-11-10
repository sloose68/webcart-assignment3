import sys
import pandas as pd
import re
import csv


#
# STEP 1
# ======
# == Script to process SOURCE excel doc and generate a flattened csv file
# == So that there are multiple rows for a doc, whenthere are multiple ecosystem
# == and/or multiple threats
# == And assign docID for each unique author/title/year
#

if len(sys.argv) != 3:
    print("Usage: python prepare-docs-dedup.py <input.xlsx> <output.csv>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

# Read your spreadsheet
df = pd.read_excel(input_file, header=0, skiprows=1)

# Replace line breaks and invalid characters in all string cells
def clean_text(x):
    if isinstance(x, str):
        x = x.replace('\n', '; ').replace('\r', '; ')
        x = x.replace('‘', "'").replace('’', "'")
        x = x.replace('“', '"').replace('”', '"')
        x = x.replace('—', '-').replace('\u00A0', ' ')
        x = re.sub(r'[^\x00-\x7F]+', '', x)  # Remove other non-ASCII chars
    return x

df = df.applymap(clean_text)

# Remove trailing spaces from column names
df.columns = df.columns.str.strip()

# Fill blanks with the last non-blank value above
df = df.ffill()

# Assign docID based on unique author/title/year
df['docID'] = df.groupby(['Authors', 'Document title', 'Year']).ngroup() + 1

# Move 'docID' to the front
cols = ['docID'] + [c for c in df.columns if c != 'docID']
df = df[cols]


# Ensure Year is integer
df['Year'] = df['Year'].astype(int)
df = df.rename(columns={"Year": "Study_year"})

# Remove duplicate rows
df = df.drop_duplicates()

# Save the result

df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

