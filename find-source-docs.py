import sys
import pandas as pd
import requests
import time

SLEEP_BETWEEN_REQUESTS = 1    

if len(sys.argv) != 3:
    print("Usage: python process-docs.py <input.xlsx> <output.xlsx>")
    sys.exit(1)

input_file  = sys.argv[1]
output_file = sys.argv[2]

try:
    df = pd.read_excel(input_file)
except:
    df = pd.read_csv(input_file)

required_cols = {"Authors", "Document title"}
if not required_cols.issubset(df.columns):
    raise ValueError("Input file must have 'author' and 'title' columns")

# --- FUNCTION TO QUERY CROSSREF ---
def get_crossref_doi(author, title):
    base_url = "https://api.crossref.org/works"
    params = {
        "query.author": author,
        "query.title": title,
        "rows": 5  # get only 5 top match
    }
    try:
        r = requests.get(base_url, params=params, timeout=30)
        r.raise_for_status()
        items = r.json().get("message", {}).get("items", [])
        # look for title (case-insensitive) so we don't get false positives
        for it in items:
            candidate_title = " ".join(it.get("title", [])).lower()
            if all(w.lower() in candidate_title for w in title.split()):
                print(f"found  {candidate_title}")
                return f"https://doi.org/{it['DOI']}"
        return None
    except Exception as e:
        print(f"Error fetching DOI for '{title}': {e}")
        return None

# --- RUN QUERY FOR EACH ROW ---
urls = []

for idx, row in df.iterrows():
    authors = row["Authors"]
    title   = row["Document title"]
    url = get_crossref_doi(authors, title)
    urls.append(url if url else "Not found")
    time.sleep(SLEEP_BETWEEN_REQUESTS)

# --- SAVE RESULTS ---
df['URL'] = urls
df.to_csv(output_file, index=False)

print(f"Done! Results saved to {output_file}")