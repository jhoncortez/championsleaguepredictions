# # import requests
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# import joblib
# import json

# #get data from football-data api. apikey required.
# # uri = 'https://api.football-data.org/v4/competitions/CL/matches'
# # headers = { 'X-Auth-Token': 'abe0c86fbb834670a6c7551e588468fb' }

# # # Load data from API
# # response = requests.get(uri = 'https://api.football-data.org/v4/competitions/CL/matches'
# #     , headers = {})
# # data = response.json()

# # # get data from ./pre-trained-data.json

# # df = pd.json_normalize('./cl-data-2024.json')

# with open('cl-data-2024.json') as f:
#     data = json.load(f)
#     # df = pd.DataFrame([data])
# # data = df.to_dict(orient='records')

# # Convert the JSON data to a Pandas DataFrame
# # matches = pd.DataFrame(data['matches'])
# # matches = pd.json_normalize(data['matches'])
# matches = data['matches']

# # lineal way, ill make it with functions later
# # matches = df["matches"]

# def getWinner(match):
#     if not match['score']['winner']:
#         return
#     if match['score']['winner'] == 'HOME_TEAM':
#         return match['homeTeam']['name']
#     if match['score']['winner'] == 'AWAY_TEAM':
#         return match['awayTeam']['name']
    

# home_teams = [match['homeTeam']['name'] for match in matches]
# away_teams = [match['awayTeam']['name'] for match in matches]
# scores = [[match['score']['fullTime']['home'], match['score']['fullTime']['away']] for match in matches]

# # X = [[
# #     match['homeTeam']['name'],
# #     match['awayTeam']['name'],
# #     match['score']['fullTime']['home'],
# #     match['score']['fullTime']['away'],

# #     ] for match in matches]
# # print(X)
# y = [getWinner(match) for match in matches]
# # print(y)

# # X = i[['homeTeam']['name'], ['awayTeam']['name'], ['score']['fullTime']['homeTeam'], ['score']['fullTime']['awayTeam']]
# # y = i['result']

# # Remove None values from y
# y = [result for result in y if result is not None]

# # Remove corresponding rows from X
# home_teams = [home_team for home_team, result in zip(home_teams, y) if result is not None]
# away_teams = [away_team for away_team, result in zip(away_teams, y) if result is not None]
# scores = [score for score, result in zip(scores, y) if result is not None]

# # Use LabelEncoder to encode the team names
# le = LabelEncoder()
# home_teams_encoded = le.fit_transform(home_teams)
# away_teams_encoded = le.fit_transform(away_teams)

# # combine the encoded teams names and scores into a list
# # X = [
# #     [home_teams_encoded,
# #     away_teams_encoded,
# #     scores[:,0],
# #     scores[:,1]] for home_team, away_team, score in zip(home_teams, away_teams, scores)]
# X = pd.DataFrame({
#     'homeTeam': home_teams_encoded, 
#     'awayTeam': away_teams_encoded, 
#     'homeTeamScore': [scores[0] for scores in scores], 
#     'awayTeamScore': [scores[0] for scores in scores]})

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # print(y_train)

# # Train a random forest classifier
# model = RandomForestClassifier(n_estimators=100, random_state=42) # 100 trees
# model.fit(X_train, y_train)

# # Save the model to a file
# joblib.dump(model, 'champions_league_model.pkl')

# # # Make predictions on the testing data
# # y_pred = model.predict(X_test)

# # # Evaluate the model
# # accuracy = accuracy_score(y_test, y_pred)
# # print(f'Accuracy: {accuracy:.3f}')

# # # Use the model to predict the outcome of a match
# # new_data = [['Team A', 'Team B', 2, 1]]
# # prediction = model.predict(new_data)
# # print(f'Predicted outcome: {prediction}')

# ## end linear way

# # # Extract relevant data from API response
# # matches = data["matches"]
# # teams = data["teams"]
# # injuries = data["injuries"]
# # head_to_head = data["head2head"]


# # # Define feature engineering function
# # def extract_features(match):
# #     team1 = match["homeTeam"]["name"]
# #     team2 = match["awayTeam"]["name"]
# #     team1_form = next((team for team in teams if team["name"] == team1), None) # Find team1 in teams
# #     team2_form = next((team for team in teams if team["name"] == team2), None) # Find team2 in teams
# #     head_to_head_data = next((x for x in head_to_head if x["team1"] == team1 and x["team2"] == team2), None)
# #     injuries_data = injuries.get(team1, []) + injuries.get(team2, [])

# #     features = {
# #         "team1_avg_goals": team1_form["avg_goals"],
# #         "team2_avg_goals": team2_form["avg_goals"],
# #         "team1_win_rate": team1_form["win_rate"],
# #         "team2_win_rate": team2_form["win_rate"],
# #         "head_to_head_team1_wins": sum(1 for x in head_to_head_data if x["winner"] == team1),
# #         "team1_key_injuries": len(injuries_data),
# #     }

# #     return features

# # # Extract features from matches
# # X = []
# # y = []
# # for match in matches:
# #     features = extract_features(match)
# #     X.append(features)
# #     y.append(match["result"])

# # # Split data into training and testing sets
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # # Scale features using StandardScaler
# # scaler = StandardScaler()
# # X_train_scaled = scaler.fit_transform(X_train)
# # X_test_scaled = scaler.transform(X_test)

# # # Train model using RandomForestClassifier
# # model = RandomForestClassifier()
# # model.fit(X_train_scaled, y_train)

# # # Evaluate model using accuracy score
# # y_pred = model.predict(X_test_scaled)
# # accuracy = accuracy_score(y_test, y_pred)
# # print("Accuracy:", accuracy)

# # # Save model to file
# # joblib.dump(model, "champions_league_model.pkl")

# # # Define predict function
# # def predict_match_outcome(team1, team2, team1_form, team2_form, head_to_head, injuries):
# #     features = extract_features({"homeTeam": {"name": team1}, "awayTeam": {"name": team2}, "result": None})
# #     features["team1_avg_goals"] = team1_form["avg_goals"]
# #     features["team2_avg_goals"] = team2_form["avg_goals"]
# #     features["team1_win_rate"] = team1_form["win_rate"]
# #     features["team2_win_rate"] = team2_form["win_rate"]
# #     features["head_to_head_team1_wins"] = sum(1 for x in head_to_head if x["winner"] == team1)
# #     features["team1_key_injuries"] = len(injuries)

# #     features_scaled = scaler.transform([features])

# #     probabilities = model.predict_proba(features_scaled)[0]

# #     return {
# #         "team1_win": float(probabilities[1]),
# #         "team2_win": float(probabilities[2]),
# #         "draw": float(probabilities[0]),
# #     }


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from app.training_data_processing import X, y
import joblib

if len(X) < 5:
    raise ValueError("Insufficient data. Need at least 5 samples.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)
joblib.dump(model, "champions_league_model.pkl")