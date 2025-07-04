# core/fetch_matches.py

from playwright.sync_api import sync_playwright
from core.utils import get_logger
import time

log = get_logger()

def fetch_matches(proxy=None, user_agent=None) -> list[dict]:
    matches = []
    url = "https://www.oddsportal.com/football/lithuania/a-lyga/zalgiris-banga-hQke26Bj/inplay-odds/"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        try:
            log.info(f"[*] Visiting match odds page: {url}")
            page.goto(url, timeout=60000)

            # Force wait for content to load
            time.sleep(5)

            # Try extracting team names from the H1
            title = page.locator("h1").first.inner_text().strip()
            if " - " not in title:
                raise Exception("Match title not in expected format.")
            team1, team2 = [x.strip() for x in title.split(" - ")]

            # Now get odds — change selector if needed
            odds_elements = page.locator("[data-odd-name]")
            count = odds_elements.count()
            odds = []

            for i in range(count):
                text = odds_elements.nth(i).inner_text().strip()
                if text:
                    odds.append(text)

            matches.append({
                "team1": team1,
                "team2": team2,
                "odds": odds,
                "match_url": url
            })

        except Exception as e:
            log.warning(f"Skipping match due to error: {e}")

        browser.close()

    return matches
