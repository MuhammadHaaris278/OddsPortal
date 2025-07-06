# core/fetch_matches.py

import pandas as pd
from core.utils import get_logger
import datetime
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta

log = get_logger()


def scrape_filtered_matches(url, sport_name, league_keywords):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        log.warning(f"Failed to fetch URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.select_one("#col-content table.table-main")
    if not table:
        return []

    matches = []
    now = dt.utcnow()
    cutoff = now + timedelta(hours=24)
    current_league = ""

    for tr in table.select("tbody > tr"):
        league_tag = tr.select_one("th > span.datet")
        if league_tag:
            current_league = league_tag.get_text(strip=True)
            continue

        if not any(keyword.lower() in current_league.lower() for keyword in league_keywords):
            continue

        time_tag = tr.select_one("td.table-time")
        teams_tag = tr.select_one("td.table-participant a")
        odds_tags = tr.select("td.odds")

        if not time_tag or not teams_tag:
            continue

        try:
            match_time_str = time_tag.get_text(strip=True)
            match_time = dt.strptime(match_time_str, "%H:%M").time()
            match_datetime = dt.combine(now.date(), match_time)
            if match_datetime < now:
                match_datetime += timedelta(days=1)

            if not (now <= match_datetime <= cutoff):
                continue

            teams = teams_tag.get_text(strip=True)
            odds = [od.get_text(strip=True) for od in odds_tags]

            matches.append({
                "datetime": match_datetime.isoformat(),
                "league": current_league,
                "teams": teams,
                "odds": odds,
                "match_url": url
            })
        except Exception as e:
            log.warning(f"Failed to parse row: {e}")
            continue

    return matches


def fetch_matches(proxy=None, user_agent=None) -> list[dict]:
    today = datetime.date.today()
    next_day = today + datetime.timedelta(days=1)
    formatted_date = next_day.strftime('%Y%m%d')

    urls = {
        "football": f"https://www.oddsportal.com/matches/football/{formatted_date}/",
        "basketball": f"https://www.oddsportal.com/matches/basketball/{formatted_date}/",
        "baseball": f"https://www.oddsportal.com/matches/baseball/{formatted_date}/",
        "futsal": f"https://www.oddsportal.com/matches/futsal/{formatted_date}/"
    }

    extra_urls = {
        "wnba": ("https://www.oddsportal.com/matches/basketball/{date}/", ["USA: WNBA"]),
        "nhl": ("https://www.oddsportal.com/hockey/usa/nhl/", ["USA: NHL"]),
        "nba": ("https://www.oddsportal.com/basketball/usa/nba/", ["USA: NBA"]),
        "premier_league": ("https://www.oddsportal.com/matches/football/{date}/", ["England: Premier League"]),
        "championship": ("https://www.oddsportal.com/matches/football/{date}/", ["England: Championship"]),
        "laliga": ("https://www.oddsportal.com/matches/football/{date}/", ["Spain: LaLiga"]),
        "laliga2": ("https://www.oddsportal.com/matches/football/{date}/", ["Spain: LaLiga2"]),
        "bundesliga": ("https://www.oddsportal.com/matches/football/{date}/", ["Germany: Bundesliga"]),
        "bundesliga2": ("https://www.oddsportal.com/matches/football/{date}/", ["Germany: 2. Bundesliga"])
    }

    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_matches = []

    for sport, url in urls.items():
        matches = []
        try:
            df = pd.read_csv('format/oddsportal.csv')
            for index, row in df.iterrows():
                try:
                    team1 = row['participant-name']
                    team2 = row['participant-name 2']
                    odds = [
                        row.get('height-content', 'N/A'),
                        row.get('height-content 2', 'N/A'),
                        row.get('height-content 3', 'N/A')
                    ]
                    matches.append({
                        "team1": team1,
                        "team2": team2,
                        "odds": odds,
                        "match_url": url
                    })
                except Exception as e:
                    log.warning(f"Skipping match due to error: {e}")

            sport_folder_path = os.path.join(output_dir, sport)
            if not os.path.exists(sport_folder_path):
                os.makedirs(sport_folder_path)

            output_csv = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.csv")
            output_json = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.json")

            matches_df = pd.DataFrame(matches)
            matches_df.to_csv(output_csv, index=False)
            with open(output_json, 'w') as json_file:
                json.dump(matches, json_file, indent=4)

            log.info(f"Saved {sport} data to CSV and JSON.")
            all_matches.extend(matches)

        except Exception as e:
            log.error(f"Error scraping {sport} data from {url}: {e}")

    for sport, (url_template, keywords) in extra_urls.items():
        url = url_template.format(
            date=formatted_date) if "{date}" in url_template else url_template
        try:
            matches = scrape_filtered_matches(url, sport, keywords)
            sport_folder_path = os.path.join(output_dir, sport)
            if not os.path.exists(sport_folder_path):
                os.makedirs(sport_folder_path)

            output_csv = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.csv")
            output_json = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.json")

            matches_df = pd.DataFrame(matches)
            matches_df.to_csv(output_csv, index=False)
            with open(output_json, 'w') as json_file:
                json.dump(matches, json_file, indent=4)

            log.info(
                f"Saved matches for {sport}.")
            all_matches.extend(matches)

        except Exception as e:
            log.error(f"Failed to scrape {sport} from {url}: {e}")

    return all_matches