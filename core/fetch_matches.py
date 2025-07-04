# core/fetch_matches.py

from core.utils import get_logger
from playwright.sync_api import sync_playwright, TimeoutError
import time

log = get_logger()

def fetch_upcoming_matches(proxy=None, user_agent=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=[
    "--disable-blink-features=AutomationControlled",
    "--start-maximized",
])
        context_args = {
            "viewport": {"width": 1920, "height": 1080}
        }

        if user_agent:
            context_args["user_agent"] = user_agent
        if proxy:
            context_args["proxy"] = {"server": proxy}

        context = browser.new_context(**context_args)
        page = context.new_page()

        matches = fetch_matches(page)

        browser.close()
        return matches


def fetch_matches(page) -> list[dict]:
    url = "https://www.oddsportal.com/inplay/"
    log.info(f"Fetching Live Soccer from {url}")
    
    try:
        page.goto(url, timeout=60000)
        time.sleep(5)  # Let JS load everything
        page.wait_for_selector(".eventRow", timeout=20000)
        rows = page.query_selector_all(".eventRow")
    except TimeoutError as te:
        log.error(f"[!] Timeout while loading page or selectors: {te}")
        return []
    except Exception as e:
        log.error(f"[!] Failed to load inplay page: {e}")
        return []

    matches = []

    for row in rows:
        try:
            link_el = row.query_selector('a[href*="/inplay-odds"]')
            team_els = row.query_selector_all('[data-testid="event-participants"] a')

            if not link_el or len(team_els) != 2:
                continue

            link = link_el.get_attribute("href")
            team1 = team_els[0].get_attribute("title")
            team2 = team_els[1].get_attribute("title")

            odds_els = row.query_selector_all('[data-testid="odd-container-default"]')
            odds = [el.inner_text() for el in odds_els if el.inner_text()]

            matches.append({
                "url": f"https://www.oddsportal.com{link}",
                "teams": f"{team1} vs {team2}",
                "odds": odds
            })

        except Exception as e:
            log.warning(f"Skipping row due to error: {e}")

    log.info(f"[+] Live Soccer: {len(matches)} matches scraped")
    return matches
