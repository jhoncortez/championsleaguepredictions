# process the data to use in model.py and create the final X and y and the .pkl file

import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import json
import numpy as np

def get_team_matches(matches, team_name):
    team_matches = []
    for match in matches:
        if match["homeTeam"]["name"] == team_name or match["awayTeam"]["name"] == team_name:
            team_matches.append(match)
    return team_matches
def calculate_team_form(matches, team_name):
    team_matches = get_team_matches(matches, team_name)
    goals = 0
    wins = 0
    # form = ""
    for match in team_matches:
        if match["homeTeam"]["name"] == team_name:
            goals += match["score"]["fullTime"]["home"] or 0
            if match["score"]["winner"] == "HOME_TEAM":
                wins += 1
        elif match["awayTeam"]["name"] == team_name:
            goals += match["score"]["fullTime"]["home"] or 0
            if match["score"]["winner"] == "AWAY_TEAM":
                wins += 1
        else:
            return {"avg_goals": 0, "win_rate": 0}
    form = {"avg_goals": goals / len(team_matches), "win_rate": wins / len(team_matches)}
    return form

def get_h2h_matches(matches, team1, team2):
    head_to_head = []
    for match in matches:
        if (match["homeTeam"]["name"] == team1 and match["awayTeam"]["name"] == team2) or (match["homeTeam"]["name"] == team2 and match["awayTeam"]["name"] == team1):
            head_to_head.append(match)
    return head_to_head

def calculate_head_to_head(matches, team1, team2):
    head_to_head = get_h2h_matches(matches, team1, team2)
    head_to_head_team1_wins = sum(1 for x in head_to_head if x["score"]["winner"] == "HOME_TEAM")
    head_to_head_team2_wins = sum(1 for x in head_to_head if x["score"]["winner"] == "AWAY_TEAM")
    return head_to_head_team1_wins, head_to_head_team2_wins
# Mock injury function (replace with real data if available)
# def get_injuries(team_name):
#     """Mock function - in reality you'd need another API"""
#     return {
#         86: ["Courtois", "Alaba"],  # Real Madrid
#         65: ["De Bruyne"]           # Man City
#     }.get(team_name, [])

# def calculate_avg_goals(matches, team_name):
#     goals = []
#     for match in matches:
#         if match["homeTeam"]["name"] == team_name:
#             goals.append(match["score"]["fullTime"]["home"])
#         elif match["awayTeam"]["name"] == team_name:
#             goals.append(match["score"]["fullTime"]["away"])
#     return np.mean(goals)

# def calculate_win_rate(matches, team_name):    
#     wins = 0
#     losses = 0
#     for match in matches:
#         if match["homeTeam"]["name"] == team_name and match["score"]["winner"] == "HOME_TEAM":
#             wins += 1
#         elif match["awayTeam"]["name"] == team_name and match["score"]["winner"] == "AWAY_TEAM":
#             wins += 1
#         elif match["homeTeam"]["name"] == team_name and match["score"]["winner"] == "AWAY_TEAM":
#             losses += 1
#         elif match["awayTeam"]["name"] == team_name and match["score"]["winner"] == "HOME_TEAM":
#             losses += 1
#     return wins / (wins + losses)
# import i

# #get data from football-data api. apikey required.
# # uri = 'https://api.football-data.org/v4/competitions/CL/matches'
# # headers = { 'X-Auth-Token': 'abe0c86fbb834670a6c7551e588468fb' }

# # # Load data from API
# # response = requests.get(uri = 'https://api.football-data.org/v4/competitions/CL/matches'
# #     , headers = {})
# # data = response.json()

# # # get data from ./pre-trained-data.json

# # df = pd.json_normalize('./cl-data-2024.json')

with open('cl-data-2024.json') as f:
    data = json.load(f)
# # # # #     df = pd.DataFrame([data])
# # # # # data = df.to_dict(orient='records')

# # # # # # Convert the JSON data to a Pandas DataFrame
# # # # # matches = pd.DataFrame(data['matches'])
# # # # # matches = pd.json_normalize(data['matches'])

# # # # # Function to get the result of a match
# # # # def getResult(match):
# # # #     if match['score']['winner'] == 'HOME_TEAM':
# # # #         return 0
# # # #     elif match['score']['winner'] == 'AWAY_TEAM':
# # # #         return 1
# # # #     else:
# # # #         return 2  # Return 2 for a draw

# # # # # # Extract relevant features
# # # # # home_teams = [match['homeTeam']['name'] for match in data['matches']]
# # # # # away_teams = [match['awayTeam']['name'] for match in data['matches']]
# # # # # scores = [[match['score']['fullTime']['home'], match['score']['fullTime']['away']] for match in data['matches']]

# # # # # # Convert scores to numpy array
# # # # # scores = np.array(scores)

# # # # # print(scores[:,0], scores[:,1])

# # # # # X = pd.DataFrame({
# # # # #     'homeTeam': home_teams, 
# # # # #     'awayTeam': away_teams, 
# # # # #     'homeTeamScore': [scores[:,0] for home_team, away_team, score in zip(home_teams, away_teams, scores)], 
# # # # #     'awayTeamScore': [scores[:,1] for home_team, away_team, score in zip(home_teams, away_teams, scores)]})

# # # # # X = pd.DataFrame({
# # # # #     'homeTeam': home_teams, 
# # # # #     'awayTeam': away_teams, 
# # # # #     'homeTeamScore': [scores[0] for scores in scores], 
# # # # #     'awayTeamScore': [scores[1] for scores in scores]}) 

# # # # # y = [getWinner(match) for match in data['matches']]




# # # # # # X = pd.DataFrame({
# # # # # #     'homeTeam': home_teams, 
# # # # # #     'awayTeam': away_teams, 
# # # # # #     'homeTeamScore': [scores[0] for scores in scores], 
# # # # # #     'awayTeamScore': [scores[1] for scores in scores]})


# # # # X = [[
# # # #     match['homeTeam']['name'],
# # # #     match['awayTeam']['name'],
# # # #     match['score']['fullTime']['home'],
# # # #     match['score']['fullTime']['away'],
# # # #     calculate_team_form(data['matches'], match['homeTeam']['name']),
# # # #     calculate_team_form(data['matches'], match['awayTeam']['name']),
# # # #     # calculate_avg_goals(data['matches'], match['homeTeam']['name']),
# # # #     # calculate_avg_goals(data['matches'], match['awayTeam']['name']),
# # # #     # calculate_win_rate(data['matches'], match['homeTeam']['name']),
# # # #     # calculate_win_rate(data['matches'], match['awayTeam']['name']),
# # # #     # calculate_head_to_head(data['matches'], match['homeTeam']['name'], match['awayTeam']['name'])
# # # #     ] for match in data['matches']]
# # # # # X = [[
# # # # #     match['homeTeam']['name'],
# # # # #     match['awayTeam']['name'],
# # # # #     match['score']['fullTime']['home'],
# # # # #     match['score']['fullTime']['away'],

# # # # #     ] for match in data['matches']]
# # # # # print(X)
# # # # # y = [getWinner(match) for match in data['matches']]
# # # # # print(y){

# # # # y = [getResult(match) for match in data['matches']]

# # # # # X = i[['homeTeam']['name'], ['awayTeam']['name'], ['score']['fullTime']['homeTeam'], ['score']['fullTime']['awayTeam']]
# # # # # y = i['result']

# # # # # Remove None values from y
# # # # y = [result for result in y if result is not None]

# # # # # # Remove corresponding rows from X
# # # # # home_teams = [home_team for home_team, result in zip(home_teams, y) if result is not None]
# # # # # away_teams = [away_team for away_team, result in zip(away_teams, y) if result is not None]
# # # # # scores = [score for score, result in zip(scores, y) if result is not None]

# # # # # # Use LabelEncoder to encode the team names
# # # # le = LabelEncoder()
# # # # home_teams = [match['homeTeam']['name'] for match in data['matches']]
# # # # away_teams = [match['awayTeam']['name'] for match in data['matches']]
# # # # home_teams_encoded = le.fit_transform(home_teams)
# # # # away_teams_encoded = le.fit_transform(away_teams)

# # # # # Convert scores to numpy array
# # # # scores = np.array([[match['score']['fullTime']['home'], match['score']['fullTime']['away']] for match in data['matches']])

# # # # # Create the final X and y
# # # # X = np.column_stack((home_teams_encoded, away_teams_encoded, scores))
# # # # y = np.array(y)

# # # # # # Split the data into training and testing sets
# # # # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # # # # print(y_train)

# # # # # Train a random forest classifier
# # # # model = RandomForestClassifier(n_estimators=100, random_state=42) # 100 trees
# # # # model.fit(X_train, y_train)

# # # # # Save the model to a file
# # # # joblib.dump(model, 'champions_league_model.pkl')

# # # # # Make predictions on the testing data
# # # # y_pred = model.predict(X_test)

# # # # # Evaluate the model
# # # # accuracy = accuracy_score(y_test, y_pred)
# # # # print(f'Accuracy: {accuracy:.3f}')

# # # # # # Use the model to predict the outcome of a match
# # # # # new_data = [['Team A', 'Team B', 2, 1]]
# # # # # prediction = model.predict(new_data)
# # # # # print(f'Predicted outcome: {prediction}')
