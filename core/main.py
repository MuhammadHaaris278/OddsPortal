# core/main.py

from utils.user_agent_pool import get_random_user_agent
from core.utils import get_logger
from core.fetch_matches import fetch_matches
import os
import sys
import json
import pandas as pd
from datetime import datetime
import random

# Fix path to allow cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logger = get_logger()


def get_rotating_proxy_and_headers():
    proxies = [
        "http://172.67.174.121:8080",
        "http://51.75.161.178:3128",
        "http://185.62.189.169:1080",
        "http://80.78.73.211:3128",
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    ]

    proxy = random.choice(proxies)
    user_agent = random.choice(user_agents)

    return proxy, user_agent


def save_results(matches):
    os.makedirs("output", exist_ok=True)

    flat = []
    for match in matches:
        flat.append({
            "sport": match.get("sport", ""),
            "team1": match.get("team1", ""),
            "team2": match.get("team2", ""),
            "odds": json.dumps(match.get("odds", {}), ensure_ascii=False),
            "match_url": match.get("match_url", "")
        })
    df = pd.DataFrame(flat)


def main():
    logger.info("[*] Starting OddsPortal Scraper...")

    proxy, ua = get_rotating_proxy_and_headers()
    logger.info(f"[*] Using proxy: {proxy}")
    logger.info(f"[*] Using UA: {ua}")

    matches = fetch_matches(proxy=proxy, user_agent=ua)
    logger.info(f"[+] Total matches scraped: {len(matches)}")

    save_results(matches)
    logger.info("[✔] Scraping complete. Data saved to /output/")


if __name__ == "__main__":
    main()
