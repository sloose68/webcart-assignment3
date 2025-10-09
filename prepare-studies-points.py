import pandas as pd
import sys

# === Script to take the modified document csv that has Long, Lat added
# === Handles multiple points added to csv as long, lat pairs
#

if len(sys.argv) != 3:
    print("Usage: python prepare-threats.py <input.csv/xlsx> <output.csv>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

# === Load input file ===
if input_file.lower().endswith(".csv"):
    df = pd.read_csv(input_file)
else:
    df = pd.read_excel(input_file)  # first sheet by default

# === Identify coordinate columns ===
# Exclude docID column; assume remaining columns alternate Long, Lat
coord_cols = [c for c in df.columns if "long" in c.lower() or "lat" in c.lower()]

records = []
for _, row in df.iterrows():
    # Step through every Long/Lat pair
    for i in range(0, len(coord_cols), 2):
        long_col = coord_cols[i]
        lat_col  = coord_cols[i+1]
        if pd.notna(row[long_col]) and pd.notna(row[lat_col]):
            records.append({
                "docID": row["docID"],
                "Long": row[long_col],
                "Lat": row[lat_col]
            })


new_df = pd.DataFrame(records)
new_df.to_csv(output_file, index=False)

print(f"file saved as: {output_file}")