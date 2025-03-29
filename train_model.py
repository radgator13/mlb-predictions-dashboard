import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from pybaseball import playerid_reverse_lookup

# === STEP 1: Load Datasets ===
print("?? Loading data...")
statcast = pd.read_csv("statcast_data.csv")
batting_stats = pd.read_csv("batting_stats.csv")

# === STEP 2: Label Target Column ===
hit_events = ['single', 'double', 'triple', 'home_run']
statcast['is_hit'] = statcast['events'].isin(hit_events).astype(int)

# === STEP 3: Convert Statcast Batter IDs to FanGraphs IDs ===
print("\n?? Converting MLBAM batter IDs to FanGraphs IDs...")
unique_batter_ids = statcast['batter'].dropna().unique()
id_mapping = playerid_reverse_lookup(unique_batter_ids, key_type='mlbam')

# 'key_mlbam' = MLBAM ID from statcast, 'key_fangraphs' = FanGraphs ID
id_mapping = id_mapping[['key_mlbam', 'key_fangraphs']]
id_mapping.columns = ['batter', 'IDfg']
id_mapping['batter'] = id_mapping['batter'].astype(int).astype(str)
id_mapping['IDfg'] = id_mapping['IDfg'].astype(str)

# Merge the ID mapping into statcast data
statcast['batter'] = statcast['batter'].astype(int).astype(str)
statcast = statcast.merge(id_mapping, on='batter', how='left')

# === STEP 4: Merge with Batting Stats Using FanGraphs ID ===
batting_stats['IDfg'] = batting_stats['IDfg'].astype(str)

print("\n?? Merging statcast with batting stats on FanGraphs ID...")
merged = statcast.merge(batting_stats, on='IDfg', how='inner')

print(f"? Rows after merge: {len(merged)}")
if merged.empty:
    print("? ERROR: Merge returned 0 rows. Check ID formats or data sources.")
    exit()

# === STEP 5: Select Features and Drop Missing ===
features = [
    'launch_speed', 'launch_angle', 'release_speed', 'effective_speed',
    'PA', 'BB%', 'K%', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+'
]

# Drop rows with missing values
data = merged[features + ['is_hit']].dropna()
print(f"\n? Rows after dropping missing values: {len(data)}")

if data.empty:
    print("? ERROR: No data available for training after cleaning.")
    exit()

X = data[features]
y = data['is_hit']

# === STEP 6: Split and Train Model ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === STEP 7: Evaluate ===
y_pred = model.predict(X_test)

print("\n? Model Training Complete")
print("\n?? Accuracy:", accuracy_score(y_test, y_pred))
print("\n?? Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model to a file
joblib.dump(model, "trained_model.pkl")
print("?? Model saved as trained_model.pkl")