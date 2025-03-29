from pybaseball import statcast, batting_stats, pitching_stats
import pandas as pd
from datetime import datetime, timedelta

# === STATCAST DATA FUNCTIONS ===

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

# === SEASON-LEVEL STATS FUNCTIONS ===

def fetch_batting_pitching_stats(season=2025):
    print(f"\nFetching season batting and pitching stats for {season}...")
    
    batting = batting_stats(season)
    pitching = pitching_stats(season)

    print(f"Batting stats: {len(batting)} rows | Pitching stats: {len(pitching)} rows")
    return batting, pitching

# === MAIN RUNNER ===

if __name__ == "__main__":
    # --- Statcast Section ---
    raw_data = fetch_statcast_data(days=3)
    if not raw_data.empty:
        cleaned_data = clean_statcast_data(raw_data)
        if not cleaned_data.empty:
            save_to_csv(cleaned_data, "statcast_data.csv")
    
    # --- Season Stats Section ---
    batting_df, pitching_df = fetch_batting_pitching_stats(season=2025)
    save_to_csv(batting_df, "batting_stats.csv")
    save_to_csv(pitching_df, "pitching_stats.csv")
