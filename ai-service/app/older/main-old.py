from fastapi import FastAPI
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


app = FastAPI()
model = joblib.load("champions_league_model.pkl")

@app.post("/predict")
def predict(team1: str, team2: str, team1_form: str, team2_form: str):
    # Feature engineering
    team1_win_rate = team1_form.count('W') / len(team1_form)
    team2_win_rate = team2_form.count('W') / len(team2_form)

    # Create a LabelEncoder for team names
    team_encoder = LabelEncoder()

    # Get unique teams
    all_teams = list(set([team1, team2]))

    # Fit the encoder to all unique team names
    team_encoder.fit(all_teams)

    # Use the encoder to transform the team names
    team1_encoded = team_encoder.transform([team1])[0]
    team2_encoded = team_encoder.transform([team2])[0]
    
    # Predict
    prediction = model.predict_proba([[team1_encoded, team2_encoded, team1_win_rate, team2_win_rate]])
    
    return {
        "team1_win": prediction[0][0],
        "team2_win": prediction[0][1],
        "draw": prediction[0][2]
    }