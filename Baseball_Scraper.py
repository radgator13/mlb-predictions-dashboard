# === imports ===
from pybaseball import statcast, batting_stats, pitching_stats
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# === functions ===

def fetch_statcast_data(days=1):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    print(f"Fetching Statcast data from {start_date.date()} to {end_date.date()}...")
    data = statcast(start_dt=start_date.strftime('%Y-%m-%d'), 
                    end_dt=end_date.strftime('%Y-%m-%d'))

    if data.empty:
        print("No Statcast data returned. Check if games were played.")
    else:
        print(f"Fetched {len(data)} rows of Statcast data.")

    return data

def clean_statcast_data(data):
    features = [
        'game_date', 'batter', 'pitcher', 'events', 'description',
        'launch_speed', 'launch_angle', 'home_team', 'away_team',
        'p_throws', 'stand', 'pitch_type', 'release_speed', 'effective_speed'
    ]

    available_features = [col for col in features if col in data.columns]

    if not available_features:
        print("No matching Statcast features found in data.")
        return pd.DataFrame()

    cleaned = data[available_features].copy()
    return cleaned

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def fetch_batting_pitching_stats(season=2025):
    print(f"\nFetching season batting and pitching stats for {season}...")

    batting = batting_stats(season)
    pitching = pitching_stats(season)

    print(f"Batting stats: {len(batting)} rows | Pitching stats: {len(pitching)} rows")
    return batting, pitching

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
    print(f"Today's games saved to todays_games.csv")
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