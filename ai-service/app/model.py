import pandas as pd
import joblib

from model_data_processing import prepare_prediction_data

# model = joblib.load("champions_league_model_3seasons.pkl")
model = joblib.load("enhanced_champions_league_model.pkl")

def predict_match(team1, team2, venue="HOME", stage=None, team1_injuries=None, team2_injuries=None):
    """Predicts match outcome (win/draw/loss probabilities)"""
    
    # Feature engineering
    features_df = prepare_prediction_data(team1, team2, venue, stage, team1_injuries, team2_injuries)
    print(f"Features for {team1} vs {team2}:", features_df)  # Add this line

    features_df.to_csv("match_features.csv", index=False)
    
    # Predict probabilities [Draw, Team1 Win, Team2 Win]
    probabilities = model.predict_proba(features_df)[0] # for classification model [0, 1, 2]
    print(f'Probabilities for {team1} vs {team2}:', probabilities)
    
    return {
        f"{team1} wins": float(probabilities[1]) * 100 ,  # Note index 1 is Team1 win
        f"{team2} wins": float(probabilities[2]) * 100,  # Index 2 is Team2 win
        "draw": float(probabilities[0]),
    }


linear_reg_model = joblib.load("cl_linear_model.pkl")
def predict_match_linear(team1, team2, venue="HOME", stage=None, team1_injuries=None, team2_injuries=None):
    """Predicts match outcome (win/draw/loss probabilities) using linear regression"""
    
    # Feature engineering
    features_df = prepare_prediction_data(team1, team2, venue, stage, team1_injuries, team2_injuries)
    print(f"Features for {team1} vs {team2}:", features_df)

    features_df.to_csv("match_features.csv", index=False)
    
    # Predict outcome score
    prediction = linear_reg_model.predict(features_df)[0]
    print(f'Prediction score for {team1} vs {team2}:', prediction)

    # Determine the outcome based on the prediction score
    if prediction > 1.5:
        result = f"{team2} wins"
    elif prediction < 0.5:
        result = f"{team1} wins"
    else:
        result = "draw"
    
    return {
        f"{team1} wins": float(prediction < 0.5),
        f"{team2} wins": float(prediction > 1.5),
        "draw": float(0.5 <= prediction <= 1.5),
        "result": result,
    }

# print(predict_match_linear("Paris Saint-Germain FC", "FC Internazionale Milano", "HOME", "FINAL", [], [])) # for linear regression

# print(predict_match("Paris Saint-Germain FC", "FC Internazionale Milano", "HOME", "FINAL", [], [])) # for classification