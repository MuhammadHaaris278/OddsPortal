# core/fetch_matches.py

from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

# Define sports and their OddsPortal slugs
SPORTS = {
    "NBA": "basketball/usa/nba",
    "WNBA": "basketball/usa/wnba",
    "MLB": "baseball/usa/mlb",
    "NHL": "hockey/usa/nhl",
    "Soccer": "soccer",
    "NFL": "american-football/usa/nfl",
    "NCAA Football": "american-football/usa/ncaa"
}

BASE_URL = "https://www.oddsportal.com"

def fetch_upcoming_matches(proxy=None, user_agent=None):
    matches = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=user_agent,
            proxy={"server": proxy} if proxy else None,
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        for sport, path in SPORTS.items():
            url = f"{BASE_URL}/{path}/"
            print(f"[*] Fetching {sport} from {url}")
            try:
                page.goto(url, timeout=30000)
                page.wait_for_timeout(3000)

                rows = page.query_selector_all("table#tournamentTable tbody tr")
                for row in rows:
                    try:
                        if "deactivate" in row.get_attribute("class", ""):
                            continue

                        time_str = row.query_selector("td.time").inner_text().strip()
                        team_str = row.query_selector("td.name a").inner_text().strip()
                        match_url = BASE_URL + row.query_selector("td.name a").get_attribute("href")

                        match_time = parse_match_time(time_str)
                        if not match_time or not is_within_24_hours(match_time):
                            continue

                        matches.append({
                            "sport": sport,
                            "teams": team_str,
                            "date_time": match_time.isoformat(),
                            "url": match_url
                        })
                    except Exception:
                        continue
                print(f"[+] {sport}: {len(matches)} matches so far...")
                time.sleep(2)
            except Exception as e:
                print(f"[!] Failed to fetch {sport}: {str(e)}")

        browser.close()
    return matches

def parse_match_time(time_str):
    try:
        today = datetime.utcnow()
        dt = datetime.strptime(time_str, "%H:%M")
        combined = today.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
        if combined < today:
            combined += timedelta(days=1)
        return combined
    except:
        return None

def is_within_24_hours(dt):
    now = datetime.utcnow()
    return now <= dt <= now + timedelta(hours=24)
