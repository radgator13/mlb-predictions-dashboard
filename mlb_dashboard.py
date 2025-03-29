import streamlit as st
import pandas as pd
from Baseball_Scraper import get_todays_games
from analyze_predictions import predict_game_outcomes
import os

# === CONFIG ===
st.set_page_config(page_title="MLB Predictions", layout="wide")
st.title("⚾ MLB Game Predictions Dashboard")

# === LOAD DATA ===
hit_df = pd.read_csv("predictions_today.csv")


if not os.path.exists("game_predictions.csv") or os.path.getsize("game_predictions.csv") == 0:
    st.warning("⚠️ No game predictions file found or file is empty. Please update today's games.")
    st.stop()

try:
    game_df = pd.read_csv("game_predictions.csv")
except pd.errors.EmptyDataError:
    st.error("❌ 'game_predictions.csv' exists but contains no readable data. Try refreshing predictions.")
    st.stop()


# === PROCESS HITS DATA ===
hits = hit_df[hit_df['predicted_hit'] == 1].copy()
hits['Team'] = hits['Team'].astype(str).str.strip().str.upper()

# === TEAM LOGO MAP (unchanged) ===
TEAM_LOGO_MAP = {
    'ATL': 'atl', 'BAL': 'bal', 'BOS': 'bos', 'CHC': 'chc', 'CIN': 'cin',
    'CLE': 'cle', 'COL': 'col', 'CWS': 'chw', 'DET': 'det', 'HOU': 'hou',
    'KCR': 'kc', 'LAA': 'laa', 'LAD': 'lad', 'MIA': 'mia', 'MIL': 'mil',
    'MIN': 'min', 'NYM': 'nym', 'NYY': 'nyy', 'OAK': 'oak', 'PHI': 'phi',
    'PIT': 'pit', 'SDP': 'sd', 'SEA': 'sea', 'SFG': 'sf', 'STL': 'stl',
    'TBR': 'tb', 'TEX': 'tex', 'TOR': 'tor', 'WSN': 'wsh'
}

# === SIDEBAR FILTERS ===
st.sidebar.header("🔍 Filter Player Results")
teams = sorted(hits['Team'].dropna().unique())
selected_team = st.sidebar.multiselect("Filter by Team", teams, default=teams)

if not selected_team:
    st.warning("Please select at least one team.")
    st.stop()

players = sorted(hits['Name'].dropna().unique())
selected_players = st.sidebar.multiselect("Filter by Player", players)

min_speed = st.sidebar.slider("Minimum Launch Speed", 60, 120, 100)
min_wrc = st.sidebar.slider("Minimum wRC+", 0, 600, 100)

# === FILTERED HITS DATA === (unchanged logic)
filtered = hits[
    hits['Team'].isin(selected_team) &
    (hits['Name'].isin(selected_players) if selected_players else True) &
    (hits['launch_speed'] >= min_speed) &
    (hits['wRC+'] >= min_wrc)
].copy()

# === DISPLAY HITS TABLE === (unchanged logic)
st.subheader("🎯 Filtered Hit Predictions")
st.dataframe(filtered[['Name', 'Team', 'launch_speed', 'wRC+', 'AVG', 'OBP']])

st.download_button(
    label="📥 Export Filtered Player Results to CSV",
    data=filtered.to_csv(index=False).encode('utf-8'),
    file_name='filtered_predictions.csv',
    mime='text/csv'
)

st.subheader("🏟️ Predicted Hits by Team")
team_chart = filtered.groupby("Team")['predicted_hit'].count().sort_values(ascending=False)
st.bar_chart(team_chart)

st.subheader("🔥 Top Hitters by wRC+")
top_wrc = filtered.sort_values(by="wRC+", ascending=False).head(10)
st.dataframe(top_wrc[['Name', 'Team', 'wRC+', 'AVG', 'OBP']])

# === GAME PREDICTIONS SECTION (UPDATED) ===
st.subheader("🎲 Predicted Game Outcomes")

if st.button("🔄 Fetch & Predict Today's Games"):
    with st.spinner("Fetching today's games and predicting outcomes..."):
        todays_games = get_todays_games()
        game_predictions = predict_game_outcomes(todays_games)
        st.success("Predictions updated!")

# Reload predictions after update
game_df = pd.read_csv("game_predictions.csv")

dates = sorted(game_df['Date'].unique())
selected_date = st.sidebar.selectbox("Select Date", dates, index=len(dates)-1)

games_filtered = game_df[game_df['Date'] == selected_date]

st.dataframe(
    games_filtered[['Home Team', 'Away Team', 'Home Win Prob', 'Away Win Prob', 'Predicted Winner', 'Predicted Total Runs']]
)

st.download_button(
    label="📥 Export Game Predictions to CSV",
    data=games_filtered.to_csv(index=False).encode('utf-8'),
    file_name='game_predictions.csv',
    mime='text/csv'
)
