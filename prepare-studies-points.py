import pandas as pd
import sys

# === Script to take the modified document excel that has Long, Lat added
# === Handles multiple points added to csv as long, lat pairs
#

if len(sys.argv) != 3:
    print("Usage: python prepare-studies-points.py <input.csv/xlsx> <output.csv>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

# === Load input file ===
if input_file.lower().endswith(".csv"):
    df = pd.read_csv(input_file)
else:
    df = pd.read_excel(input_file)  # first sheet by default

# Replace line breaks (\n and \r) with '; ' in all string cells
df = df.applymap(
    lambda x: x.replace('\n', '; ').replace('\r', '; ') if isinstance(x, str) else x
)
# === Identify coordinate columns ===
# Exclude docID column; assume remaining columns alternate Long, Lat
coord_cols = [c for c in df.columns if "long" in c.lower() or "lat" in c.lower()]

records = []
for _, row in df.iterrows():
    for i in range(0, len(coord_cols), 2):
        long_col = coord_cols[i]
        lat_col  = coord_cols[i+1]
        long_val = row[long_col]
        lat_val  = row[lat_col]

        # Check presence
        if pd.notna(long_val) and pd.notna(lat_val):
            # Try converting to float
            try:
                long_num = float(long_val)
                lat_num  = float(lat_val)
            except ValueError:
                print(f"⚠️ Skipped docID {row['docID']} — non-numeric values: Long='{long_val}', Lat='{lat_val}'")
                continue

            # Check length (as string) and value ranges
            if len(str(long_val)) >= 3 and len(str(lat_val)) >= 3:
                records.append({
                    "docID": row["docID"],
                    "Long": long_num,
                    "Lat": lat_num
                })
            else:
                print(f"⚠️ Skipped docID {row['docID']} — values too short: Long='{long_val}', Lat='{lat_val}'")
        else:
            print(f"⚠️ Skipped docID {row['docID']} — missing coordinate(s): Long='{long_val}', Lat='{lat_val}'")

new_df = pd.DataFrame(records)
new_df.to_csv(output_file, index=False)
print(f"✅ Done! Wrote {len(new_df)} valid coordinate rows to {output_file}")