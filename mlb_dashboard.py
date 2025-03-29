import streamlit as st
import pandas as pd

# === CONFIG ===
st.set_page_config(page_title="MLB Predictions", layout="wide")
st.title("⚾ MLB Game Predictions Dashboard")

# === LOAD DATA ===
hit_df = pd.read_csv("predictions_today.csv")
game_df = pd.read_csv("game_predictions.csv")

# === PROCESS HITS DATA ===
hits = hit_df[hit_df['predicted_hit'] == 1].copy()
hits['Team'] = hits['Team'].astype(str).str.strip().str.upper()

# === TEAM LOGO MAP ===
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

# === FILTERED HITS DATA ===
filtered = hits[
    hits['Team'].isin(selected_team) &
    (hits['Name'].isin(selected_players) if selected_players else True) &
    (hits['launch_speed'] >= min_speed) &
    (hits['wRC+'] >= min_wrc)
].copy()

# === ADD LOGOS AND HEADSHOTS ===
def get_team_logo(team_abbr):
    code = TEAM_LOGO_MAP.get(team_abbr)
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{code}.png" if code else ""

filtered["Team Logo"] = filtered["Team"].apply(get_team_logo)
filtered["Headshot URL"] = filtered["batter"].apply(
    lambda x: f"https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/{x}/headshot/67/current.png"
)
filtered["Logo"] = filtered["Team Logo"].apply(lambda url: f'<img src="{url}" width="40">')
filtered["Headshot"] = filtered["Headshot URL"].apply(lambda url: f'<img src="{url}" width="50">')

# === HOT HITTER TAGS ===
def tag_hot_hitter(wrc):
    if wrc >= 180:
        return "🔥🔥 Hot"
    elif wrc >= 130:
        return "🔥 Warm"
    elif wrc >= 100:
        return "🌡️ Average"
    else:
        return "🧊 Cold"

filtered["Status"] = filtered["wRC+"].apply(tag_hot_hitter)

# === DISPLAY HITS TABLE ===
st.subheader("🎯 Filtered Hit Predictions")

styled = filtered[['Headshot', 'Name', 'Status', 'Team', 'Logo', 'launch_speed', 'wRC+', 'AVG', 'OBP']]
styled.columns = ['Player', 'Name', 'Status', 'Team', 'Team', 'Launch Speed', 'wRC+', 'AVG', 'OBP']

st.markdown(
    styled.to_html(escape=False, index=False),
    unsafe_allow_html=True
)

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

# === GAME PREDICTIONS SECTION ===
st.subheader("🎲 Predicted Game Outcomes")

st.sidebar.header("📊 Filter Game Predictions")
dates = sorted(game_df['Date'].unique())
selected_date = st.sidebar.selectbox("Select Date", dates, index=len(dates)-1)
selected_game_teams = st.sidebar.multiselect(
    "Filter by Team",
    sorted(set(game_df['Home Team'].unique()).union(set(game_df['Away Team'].unique())))
)

games_filtered = game_df[game_df['Date'] == selected_date].copy()
if selected_game_teams:
    games_filtered = games_filtered[
        games_filtered['Home Team'].isin(selected_game_teams) |
        games_filtered['Away Team'].isin(selected_game_teams)
    ]

games_filtered['Winner'] = games_filtered['Predicted Winner'].apply(lambda x: f"✅ {x}")
games_filtered['Total Runs'] = games_filtered['Predicted Total Runs']

st.dataframe(
    games_filtered[['Home Team', 'Away Team', 'Home Win Prob', 'Away Win Prob', 'Winner', 'Total Runs']]
)

st.download_button(
    label="📥 Export Game Predictions to CSV",
    data=games_filtered.to_csv(index=False).encode('utf-8'),
    file_name='game_predictions.csv',
    mime='text/csv'
)
