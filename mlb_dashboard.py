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

# === GAME PREDICTIONS SECTION (UPDATED) ===
st.subheader("🎲 Predicted Game Outcomes")

if st.button("🔄 Fetch & Predict Today's Games"):
    with st.spinner("Fetching today's games and predicting outcomes..."):
        todays_games = get_todays_games()

        if todays_games.empty:
            st.warning("⚠️ No games found today. Check ESPN schedule.")
            st.stop()

        game_predictions = predict_game_outcomes(todays_games)

        if game_predictions.empty:
            st.warning("⚠️ No predictions generated. Check your model or inputs.")
            st.stop()

        st.success("✅ Predictions updated!")

# ✅ Now we check and load the file AFTER trying to generate it
if not os.path.exists("game_predictions.csv") or os.path.getsize("game_predictions.csv") == 0:
    st.warning("⚠️ No game predictions file found or file is empty. Please update today's games.")
    st.stop()

try:
    game_df = pd.read_csv("game_predictions.csv")
except pd.errors.EmptyDataError:
    st.error("❌ 'game_predictions.csv' exists but contains no readable data. Try refreshing predictions.")
    st.stop()

# === FILTER GAME DATA ===
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

