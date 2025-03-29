import pandas as pd
import joblib
import numpy as np

def predict_game_outcomes(df):
    # Load your trained prediction model
    model = joblib.load('trained_model.pkl')

    predictions = []
    for _, row in df.iterrows():
        home_team, away_team = row['Home Team'], row['Away Team']
        
        # Placeholder logic: Replace this with your real feature extraction!
        features = np.random.rand(1, 10)

        predicted_scores = model.predict(features)
        home_score, away_score = predicted_scores[0]

        winner = home_team if home_score >= away_score else away_team
        predictions.append({
            'Date': row['Date'],
            'Home Team': home_team,
            'Away Team': away_team,
            'Home Predicted Score': round(home_score, 1),
            'Away Predicted Score': round(away_score, 1),
            'Home Win Prob': round(np.random.uniform(0.5, 0.8), 2),
            'Away Win Prob': round(np.random.uniform(0.2, 0.5), 2),
            'Predicted Winner': winner,
            'Predicted Total Runs': round(home_score + away_score, 1)
        })

    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv("game_predictions.csv", index=False)
    print("✅ Game predictions saved to game_predictions.csv")
    return predictions_df
