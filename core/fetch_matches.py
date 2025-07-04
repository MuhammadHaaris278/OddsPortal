# core/fetch_matches.py

import pandas as pd
from core.utils import get_logger

log = get_logger()


def fetch_matches(proxy=None, user_agent=None) -> list[dict]:
    matches = []
    url = "https://www.oddsportal.com/matches/football/20250706/"  # The specific match URL

    try:
        # Specify the full path to the CSV file
        # Full path to CSV file
        df = pd.read_csv(
            'C:/Users/muham/OneDrive/Desktop/New folder/OddsPortal-scraper/oddsportal.csv')

        # Extract relevant columns
        for index, row in df.iterrows():
            try:
                # Extract team names
                team1 = row['participant-name']
                team2 = row['participant-name 2']

                # Extract odds (adjust this logic as necessary based on your CSV)
                odds = [
                    row.get('height-content', 'N/A'),
                    row.get('height-content 2', 'N/A'),
                    row.get('height-content 3', 'N/A')
                ]

                # If the match data is available, add it to the matches list
                matches.append({
                    "team1": team1,
                    "team2": team2,
                    "odds": odds,
                    "match_url": url
                })

            except Exception as e:
                log.warning(f"Skipping match due to error: {e}")

    except Exception as e:
        log.error(f"Error reading CSV: {e}")

    log.info(f"[+] Total matches scraped: {len(matches)}")
    return matches
