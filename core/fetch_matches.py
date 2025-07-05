# core/fetch_matches.py

import pandas as pd
from core.utils import get_logger
import datetime
import os
import json

log = get_logger()


def fetch_matches(proxy=None, user_agent=None) -> list[dict]:
    # Get today's date and calculate the next day's date
    today = datetime.date.today()
    next_day = today + datetime.timedelta(days=1)
    formatted_date = next_day.strftime('%Y%m%d')  # Format the date as YYYYMMDD

    # URLs for Football, Basketball, Baseball, and Futsal with dynamically updated date
    urls = {
        "football": f"https://www.oddsportal.com/matches/football/{formatted_date}/",
        "basketball": f"https://www.oddsportal.com/matches/basketball/{formatted_date}/",
        "baseball": f"https://www.oddsportal.com/matches/baseball/{formatted_date}/",
        "futsal": f"https://www.oddsportal.com/matches/futsal/{formatted_date}/"
    }

    # Ensure the parent output folder exists
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through each sport URL and scrape the matches
    for sport, url in urls.items():
        matches = []  # Reset the matches list for each sport
        try:
            # Read the CSV file (make sure to adjust the path if needed)
            df = pd.read_csv('format/oddsportal.csv')  # Adjusted file path

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

            # Ensure the folder for the sport exists, create it if not
            sport_folder_path = os.path.join(output_dir, sport)
            if not os.path.exists(sport_folder_path):
                os.makedirs(sport_folder_path)

            # Save the matches to both CSV and JSON files in the respective folder
            output_csv = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.csv")
            output_json = os.path.join(
                sport_folder_path, f"{sport}_{formatted_date}.json")

            # Save to CSV
            matches_df = pd.DataFrame(matches)
            matches_df.to_csv(output_csv, index=False)
            log.info(f"Saved {sport} data to CSV at {output_csv}")

            # Save to JSON
            with open(output_json, 'w') as json_file:
                json.dump(matches, json_file, indent=4)
            log.info(f"Saved {sport} data to JSON at {output_json}")

        except Exception as e:
            log.error(f"Error scraping {sport} data from {url}: {e}")

    log.info(f"[+] Total matches scraped: {len(matches)}")
    return matches
