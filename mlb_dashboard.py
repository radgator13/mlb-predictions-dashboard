import streamlit as st
import pandas as pd

# === CONFIG ===
st.set_page_config(page_title="MLB Predictions", layout="wide")
st.title("? MLB Predicted Hitters Dashboard")

# === LOAD DATA ===
df = pd.read_csv("predictions_today.csv")
hits = df[df['predicted_hit'] == 1]

# === TEAM LOGO MAP ===
TEAM_LOGO_MAP = {
    'ATL': 'atl', 'BAL': 'bal', 'BOS': 'bos', 'CHC': 'chc', 'CIN': 'cin',
    'CLE': 'cle', 'COL': 'col', 'CWS': 'chw', 'DET': 'det', 'HOU': 'hou',
    'KCR': 'kc', 'LAA': 'laa', 'LAD': 'lad', 'MIA': 'mia', 'MIL': 'mil',
    'MIN': 'min', 'NYM': 'nym', 'NYY': 'nyy', 'OAK': 'oak', 'PHI': 'phi',
    'PIT': 'pit', 'SDP': 'sd', 'SEA': 'sea', 'SFG': 'sf', 'STL': 'stl',
    'TBR': 'tb', 'TEX': 'tex', 'TOR': 'tor', 'WSN': 'wsh'
}

# === FILTER SIDEBAR ===
st.sidebar.header("?? Filter Results")

teams = sorted(hits['Team'].dropna().unique())
selected_team = st.sidebar.multiselect("Filter by Team", teams, default=teams)

players = sorted(hits['Name'].dropna().unique())
selected_players = st.sidebar.multiselect("Filter by Player", players)

min_speed = st.sidebar.slider("Minimum Launch Speed", 60, 120, 100)
min_wrc = st.sidebar.slider("Minimum wRC+", 0, 600, 100)

# === FILTERED DATA ===
filtered = hits[
    (hits['Team'].isin(selected_team)) &
    (hits['Name'].isin(selected_players) if selected_players else True) &
    (hits['launch_speed'] >= min_speed) &
    (hits['wRC+'] >= min_wrc)
]

# === ADD LOGO URL COLUMN ===
def get_team_logo(team_abbr):
    code = TEAM_LOGO_MAP.get(team_abbr)
    if code:
        return f"https://a.espncdn.com/i/teamlogos/mlb/500/{code}.png"
    return ""

filtered["Team Logo"] = filtered["Team"].apply(get_team_logo)

# === DISPLAY FILTERED TABLE WITH LOGOS ===
st.subheader("?? Filtered Predictions")

styled = filtered[['Name', 'Team', 'Team Logo', 'launch_speed', 'wRC+']].copy()
styled['Logo'] = styled['Team Logo'].apply(lambda url: f'<img src="{url}" width="40">')


st.markdown(
    styled[['Logo', 'Name', 'Team', 'launch_speed', 'wRC+']].to_html(escape=False, index=False),
    unsafe_allow_html=True
)



# === TEAM BAR CHART ===
st.subheader("??? Predicted Hits by Team")
team_chart = filtered.groupby("Team")['predicted_hit'].count().sort_values(ascending=False)
st.bar_chart(team_chart)

# === TOP HITTERS BY wRC+ ===
st.subheader("?? Top Hitters by wRC+")
top_wrc = filtered.sort_values(by="wRC+", ascending=False).head(10)
st.dataframe(top_wrc[['Name', 'Team', 'wRC+', 'AVG', 'OBP']])
