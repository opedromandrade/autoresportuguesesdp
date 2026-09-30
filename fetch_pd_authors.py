#!/usr/bin/env python3
"""
Fetch Portuguese authors whose works are in the public domain (as of 2026)
from Wikidata, and export to CSV.
"""

import sys
import csv
import requests
from pathlib import Path

# ---- Configuration ----
ENDPOINT = "https://query.wikidata.org/sparql"
OUTPUT_FILE = Path("portuguese_authors_public_domain.csv")
CURRENT_YEAR = 2026
USER_AGENT = "PortugueseAuthorsPD/1.0 (your-email@example.com)"

QUERY = f"""
SELECT DISTINCT ?label ?qid ?wikidataUrl ?wikipediaUrl ?dateOfBirth ?dateOfDeath ?publicDomainYear WHERE {{
  ?author wdt:P31 wd:Q5 ;
          wdt:P27 wd:Q45 ;
          wdt:P569 ?dateOfBirth ;
          wdt:P570 ?dateOfDeath ;
          rdfs:label ?label .
  FILTER(LANG(?label) = "pt")

  BIND(STRAFTER(STR(?author), "entity/") AS ?qid)
  BIND(CONCAT("https://www.wikidata.org/wiki/", ?qid) AS ?wikidataUrl)

  OPTIONAL {{
    ?wikipediaArticle schema:about ?author ;
                      schema:isPartOf <https://pt.wikipedia.org/> .
  }}
  BIND(COALESCE(STR(?wikipediaArticle), "-") AS ?wikipediaUrl)

  BIND(YEAR(?dateOfDeath) + 71 AS ?publicDomainYear)
  FILTER(?publicDomainYear <= {CURRENT_YEAR})
}}
ORDER BY ?label
LIMIT 5000
"""

def main():
    print(f"Querying Wikidata for Portuguese public-domain authors (<= {CURRENT_YEAR})...")

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/csv",
    }

    try:
        response = requests.get(
            ENDPOINT,
            params={"query": QUERY},
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Wikidata: {e}", file=sys.stderr)
        sys.exit(1)

    # Write CSV
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        f.write(response.text)

    # Count rows (minus header)
    rows = sum(1 for _ in response.text.splitlines()) - 1
    print(f"Done. {rows} authors written to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()