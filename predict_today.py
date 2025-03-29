import pandas as pd
from pybaseball import playerid_reverse_lookup
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# === STEP 1: Load Today's Statcast Data ===
print("?? Loading today's statcast data...")
today_data = pd.read_csv("statcast_data.csv")

# === STEP 2: Convert Batter IDs to FanGraphs IDs ===
print("?? Converting batter IDs to FanGraphs IDs...")
unique_batter_ids = today_data['batter'].dropna().unique()
id_mapping = playerid_reverse_lookup(unique_batter_ids, key_type='mlbam')
id_mapping = id_mapping[['key_mlbam', 'key_fangraphs']]
id_mapping.columns = ['batter', 'IDfg']
id_mapping['batter'] = id_mapping['batter'].astype(int).astype(str)
id_mapping['IDfg'] = id_mapping['IDfg'].astype(str)

today_data['batter'] = today_data['batter'].astype(int).astype(str)
today_data = today_data.merge(id_mapping, on='batter', how='left')

# === STEP 3: Load Batting Stats ===
batting_stats = pd.read_csv("batting_stats.csv")
batting_stats['IDfg'] = batting_stats['IDfg'].astype(str)

# === STEP 4: Merge Data ===
merged = today_data.merge(batting_stats, on='IDfg', how='inner')
print(f"? Merged rows: {len(merged)}")

# === STEP 5: Select Features ===
features = [
    'launch_speed', 'launch_angle', 'release_speed', 'effective_speed',
    'PA', 'BB%', 'K%', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+'
]

X = merged[features].dropna()
print(f"?? Rows with usable features: {len(X)}")

if X.empty:
    print("? No usable data for prediction. Exiting.")
    exit()

# === STEP 6: Load the Real Trained Model ===
print("?? Loading trained model...")
model = joblib.load("trained_model.pkl")
print("? Model loaded successfully.")

# === STEP 7: Predict and Save Results ===
predictions = model.predict(X)
prediction_df = merged.loc[X.index].copy()
prediction_df['predicted_hit'] = predictions

# === STEP 8: Save Output ===
output_path = "predictions_today.csv"
prediction_df.to_csv(output_path, index=False)
print(f"?? Predictions saved to: {os.path.abspath(output_path)}")

