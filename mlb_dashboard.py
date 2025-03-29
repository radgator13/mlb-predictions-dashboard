import streamlit as st
import pandas as pd

# Load the prediction data
df = pd.read_csv("predictions_today.csv")

st.title("? MLB Predicted Hitters Dashboard")

# Summary Stats
st.subheader("Prediction Summary")
hit_counts = df['predicted_hit'].value_counts().to_dict()
st.write(f"? Predicted Hits: {hit_counts.get(1, 0)}")
st.write(f"? Predicted Outs: {hit_counts.get(0, 0)}")

# Filter for predicted hits
hits = df[df['predicted_hit'] == 1]

# Top hitters by launch speed
st.subheader("?? Top Hitters by Launch Speed")
st.dataframe(hits.sort_values(by="launch_speed", ascending=False).head(10)[['Name', 'Team', 'launch_speed', 'wRC+']])

# Top hitters by wRC+
st.subheader("?? Top Hitters by wRC+")
st.dataframe(hits.sort_values(by="wRC+", ascending=False).head(10)[['Name', 'Team', 'wRC+', 'AVG']])

# Team hit count
st.subheader("??? Teams with Most Predicted Hits")
team_hits = hits.groupby('Team')['predicted_hit'].count().sort_values(ascending=False).head(10)
st.bar_chart(team_hits)
