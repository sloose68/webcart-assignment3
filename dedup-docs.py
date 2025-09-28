#!/usr/bin/env python3
import sys
import pandas as pd

def main():
    if len(sys.argv) != 3:
        print("Usage: python process-docs.py <input.xlsx> <output.xlsx>")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    # Read Excel input - ignore first row
    df = pd.read_excel(input_file, header=0, skiprows=1)
    # Strip leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Keep only the first N columns (change N as needed)
    N = 5
    df = df.iloc[:, :N]

    # Drop duplicates based on the first three columns, keeping the first occurrence

    df = df.drop_duplicates(subset=df.columns[:3], keep='first').reset_index(drop=True)  
 
    # Save to new csv file
    df.to_csv(output_file, index=False)

    print(f"Wrote {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()