import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

#get data from football-data api. apikey required. 
uri = 'https://api.football-data.org/v4/competitions/CL/matches'
# headers = { 'X-Auth-Token': 'abe0c86fbb834670a6c7551e588468fb' }

# # Load data from API
# response = requests.get(uri = 'https://api.football-data.org/v4/competitions/CL/matches'
#     , headers = {})
# data = response.json()

# # get data from ./pre-trained-data.json   

# df = pd.read_json('./cl-data-2024.json')
response = requests.get(uri, headers=headers)
data = response.json()

if not data["matches"]:
    print("No matches found")
    # You can add some additional logic here to handle the case where no matches are found
    exit()
    else: 
        for match in response.json()['matches']:
            print match

        exit()

# Extract relevant data from API response
matches = data["matches"]
teams = data["teams"]
injuries = data["injuries"]
head_to_head = data["head2head"]


# Define feature engineering function
def extract_features(match):
    team1 = match["homeTeam"]["name"]
    team2 = match["awayTeam"]["name"]
    team1_form = next((team for team in teams if team["name"] == team1), None) # Find team1 in teams
    team2_form = next((team for team in teams if team["name"] == team2), None) # Find team2 in teams
    head_to_head_data = next((x for x in head_to_head if x["team1"] == team1 and x["team2"] == team2), None)
    injuries_data = injuries.get(team1, []) + injuries.get(team2, [])
    
    features = {
        "team1_avg_goals": team1_form["avg_goals"],
        "team2_avg_goals": team2_form["avg_goals"],
        "team1_win_rate": team1_form["win_rate"],
        "team2_win_rate": team2_form["win_rate"],
        "head_to_head_team1_wins": sum(1 for x in head_to_head_data if x["winner"] == team1),
        "team1_key_injuries": len(injuries_data),
    }
    
    return features

# Extract features from matches
X = []
y = []
for match in matches:
    features = extract_features(match)
    X.append(features)
    y.append(match["result"])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model using RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

# Evaluate model using accuracy score
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save model to file
joblib.dump(model, "champions_league_model.pkl")

# Define predict function
def predict_match_outcome(team1, team2, team1_form, team2_form, head_to_head, injuries):
    features = extract_features({"homeTeam": {"name": team1}, "awayTeam": {"name": team2}, "result": None})
    features["team1_avg_goals"] = team1_form["avg_goals"]
    features["team2_avg_goals"] = team2_form["avg_goals"]
    features["team1_win_rate"] = team1_form["win_rate"]
    features["team2_win_rate"] = team2_form["win_rate"]
    features["head_to_head_team1_wins"] = sum(1 for x in head_to_head if x["winner"] == team1)
    features["team1_key_injuries"] = len(injuries)
    
    features_scaled = scaler.transform([features])
    
    probabilities = model.predict_proba(features_scaled)[0]
    
    return {
        "team1_win": float(probabilities[1]),
        "team2_win": float(probabilities[2]),
        "draw": float(probabilities[0]),
    }