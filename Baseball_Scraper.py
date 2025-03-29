# === imports ===
from pybaseball import statcast, batting_stats, pitching_stats
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# === functions ===

def fetch_statcast_data(days=1):
    ...

def clean_statcast_data(data):
    ...

def save_to_csv(data, filename):
    ...

def fetch_batting_pitching_stats(season=2025):
    ...

def get_todays_games():
    today = datetime.now().strftime('%Y%m%d')
    url = f"https://www.espn.com/mlb/schedule/_/date/{today}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []
    for event in soup.select('.Schedule__Table tbody tr'):
        teams = event.select('a.AnchorLink')
        if len(teams) >= 2:
            away_team = teams[0].text.strip()
            home_team = teams[1].text.strip()
            games.append({
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Away Team': away_team,
                'Home Team': home_team
            })

    games_df = pd.DataFrame(games)
    games_df.to_csv("todays_games.csv", index=False)
    return games_df

# === main runner ===
if __name__ == "__main__":
    raw_data = fetch_statcast_data(days=3)
    if not raw_data.empty:
        cleaned_data = clean_statcast_data(raw_data)
        if not cleaned_data.empty:
            save_to_csv(cleaned_data, "statcast_data.csv")

    batting_df, pitching_df = fetch_batting_pitching_stats(season=2025)
    save_to_csv(batting_df, "batting_stats.csv")
    save_to_csv(pitching_df, "pitching_stats.csv")
