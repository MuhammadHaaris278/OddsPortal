import os
import sys
import json
import pandas as pd
from datetime import datetime

# Fix path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.fetch_matches import fetch_matches
from core.utils import get_logger
from utils.proxy_pool import get_random_proxy
from utils.user_agent_pool import get_random_user_agent

logger = get_logger()

def save_results(matches):
    os.makedirs("output", exist_ok=True)

    # Save JSON
    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)

    # Save CSV
    flat = []
    for match in matches:
        flat.append({
            "team1": match.get("team1", ""),
            "team2": match.get("team2", ""),
            "odds": json.dumps(match.get("odds", {}), ensure_ascii=False),
            "match_url": match.get("match_url", "")
        })
    df = pd.DataFrame(flat)
    df.to_csv("output/results.csv", index=False)

def main():
    logger.info("[*] Starting OddsPortal Scraper...")

    proxy = None  # You can add rotating proxy logic if needed
    ua = get_random_user_agent()
    logger.info(f"[*] Using proxy: {proxy}")
    logger.info(f"[*] Using UA: {ua}")

    matches = fetch_matches(proxy=proxy, user_agent=ua)
    logger.info(f"[+] Total matches scraped: {len(matches)}")

    save_results(matches)
    logger.info("[✔] Scraping complete. Data saved to /output/")

if __name__ == "__main__":
    main()
