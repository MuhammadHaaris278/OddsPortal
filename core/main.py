# core/main.py

from core.fetch_matches import fetch_upcoming_matches
from core.parse_odds import extract_markets
from core.filter_soccer_leagues import filter_soccer
from utils.proxy_pool import get_random_proxy
from utils.user_agent_pool import get_random_user_agent
import pandas as pd
import json
from datetime import datetime
import os

def save_results(matches):
    # Save to JSON
    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)

    # Save to CSV
    flat = []
    for match in matches:
        flat.append({
            "sport": match["sport"],
            "teams": match["teams"],
            "date_time": match["date_time"],
            "market": match["market"],
            "odds": match["odds"]
        })
    pd.DataFrame(flat).to_csv("output/results.csv", index=False)

def main():
    print("[*] Starting OddsPortal Scraper...")

    proxy = get_random_proxy()
    ua = get_random_user_agent()
    print(f"[*] Using proxy: {proxy}")
    print(f"[*] Using UA: {ua}")

    matches = fetch_upcoming_matches(proxy=proxy, user_agent=ua)
    print(f"[+] Fetched {len(matches)} total matches")

    filtered = filter_soccer(matches)
    print(f"[+] {len(filtered)} soccer matches kept after tier filtering")

    for match in filtered:
        match["market"], match["odds"] = extract_markets(match["url"], proxy, ua)

    save_results(filtered)
    print("[✔] Scraping complete. Data saved to output/")

if __name__ == "__main__":
    main()
