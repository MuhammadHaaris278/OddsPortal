import os
import sys
import json
import pandas as pd
from datetime import datetime

# Fix sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.fetch_matches import fetch_matches
from core.utils import get_logger
from utils.proxy_pool import get_random_proxy
from utils.user_agent_pool import get_random_user_agent

logger = get_logger()

def save_results(matches):
    with open("output/results.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)

    flat = []
    for match in matches:
        flat.append({
            "team1": match["team1"],
            "team2": match["team2"],
            "odds": ", ".join(match["odds"]),
            "match_url": match["match_url"],
        })
    pd.DataFrame(flat).to_csv("output/results.csv", index=False)

def main():
    logger.info("[*] Starting OddsPortal Scraper...")

    proxy = None
    ua = get_random_user_agent()
    logger.info(f"[*] Using proxy: {proxy}")
    logger.info(f"[*] Using UA: {ua}")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(user_agent=ua)
        page = context.new_page()

        matches = fetch_matches(page)
        logger.info(f"[+] Total matches scraped: {len(matches)}")

        save_results(matches)

        browser.close()
        logger.success("[✔] Scraping complete. Data saved to /output/")

if __name__ == "__main__":
    main()
