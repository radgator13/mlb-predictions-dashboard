import pandas as pd

# Load your predictions file
df = pd.read_csv("predictions_today.csv")

# Basic summary
print(f"\n?? Total rows: {len(df)}")
print(f"? Predictions made: {df['predicted_hit'].value_counts().to_dict()}")

# === Top Hitters by Launch Speed (Predicted Hit Only) ===
top_speed = df[df['predicted_hit'] == 1].sort_values(by='launch_speed', ascending=False).head(10)
print("\n?? Top Predicted Hitters by Launch Speed:")
print(top_speed[['Name', 'Team', 'launch_speed', 'wRC+']])

# === Top Hitters by wRC+ (Predicted Hit Only) ===
top_wrc = df[df['predicted_hit'] == 1].sort_values(by='wRC+', ascending=False).head(10)
print("\n?? Top Predicted Hitters by wRC+:")
print(top_wrc[['Name', 'Team', 'wRC+', 'AVG']])

# === Predicted Hits Per Team ===
team_hits = df[df['predicted_hit'] == 1].groupby('Team')['predicted_hit'].count().sort_values(ascending=False)
print("\n??? Predicted Hits by Team:")
print(team_hits.head(10))
