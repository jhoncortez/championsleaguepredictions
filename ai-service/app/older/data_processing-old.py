# import pandas as pd
# from sklearn.preprocessing import LabelEncoder

# # Load and clean data
# df = pd.read_csv("matches.csv")
# valid_winners = ["team1", "team2", "draw"]
# df = df[df["winner"].isin(valid_winners)]  # Drop invalid rows

# # Exit if no data left
# if len(df) < 5:
#     raise ValueError("Not enough valid data (need at least 5 matches).")

# # Encode teams
# all_teams = pd.unique(df[["team1", "team2"]].values.ravel())
# encoder = LabelEncoder()
# encoder.fit(all_teams)
# df["team1_encoded"] = encoder.transform(df["team1"])
# df["team2_encoded"] = encoder.transform(df["team2"])

# # Feature engineering
# df["team1_win_rate"] = df["team1_form"].apply(lambda x: x.count('W') / 5)
# df["team2_win_rate"] = df["team2_form"].apply(lambda x: x.count('W') / 5)

# # Define X and y
# X = df[["team1_encoded", "team2_encoded", "team1_win_rate", "team2_win_rate"]]
# y = df["winner"].map({"team1": 0, "team2": 1, "draw": 2})

# print("Final X shape:", X.shape)
# print("Final y shape:", y.shape)

import requests
import pandas as pd
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# API Setup
# url = "https://api.football-data.org/v4/competitions/CL/matches"
# headers = {"X-Auth-Token": "YOUR_API_KEY"}  # Get a free key at https://www.football-data.org/

# Fetch 2025 matches (season 2024/25)
# response = requests.get(url, headers=headers, params={"season": 2024})
# data = response.json()

def calculate_team_form(matches, team_name):
    form = ""
    for match in matches:
        if match["homeTeam"]["name"] == team_name:
            form += "W" if match["score"]["winner"] == "HOME_TEAM" else "L"
        elif match["awayTeam"]["name"] == team_name:
            form += "W" if match["score"]["winner"] == "AWAY_TEAM" else "L"
        else:
            form += "D"
    return form

# due that I already have the downloaded data from the api as json file i will load it
with open('cl-data-2024.json') as f:
    data = json.load(f)

# Convert to DataFrame
matches = []
for match in data["matches"]:
    matches.append({
        "date": match["utcDate"],
        "team1": match["homeTeam"]["name"],
        "team2": match["awayTeam"]["name"],
        "team1_goals": match["score"]["fullTime"]["home"],
        "team2_goals": match["score"]["fullTime"]["away"],
        "winner": "team1" if match["score"]["winner"] == "HOME_TEAM" else ("team2" if match["score"]["winner"] == "AWAY_TEAM" else "draw"),
        "team1_form": calculate_team_form(data["matches"], match["homeTeam"]["name"]),  # Replace with real form (see Option B)
        "team2_form": calculate_team_form(data["matches"], match["awayTeam"]["name"]),   # Replace with real form
    })

df = pd.DataFrame(matches)
# df.to_csv("cl_2025_matches.csv", index=False)

valid_winners = ["team1", "team2", "draw"]
df = df[df["winner"].isin(valid_winners)]  # Drop invalid rows

# Exit if no data left
if len(df) < 5:
    raise ValueError("Not enough valid data (need at least 5 matches).")

# Encode teams
all_teams = pd.unique(df[["team1", "team2"]].values.ravel())
encoder = LabelEncoder()
encoder.fit(all_teams)
df["team1_encoded"] = encoder.transform(df["team1"])
df["team2_encoded"] = encoder.transform(df["team2"])

# Feature engineering
df["team1_win_rate"] = df["team1_form"].apply(lambda x: x.count('W') / 5)
df["team2_win_rate"] = df["team2_form"].apply(lambda x: x.count('W') / 5)

# Define X and y
X = df[["team1_encoded", "team2_encoded", "team1_win_rate", "team2_win_rate"]]
y = df["winner"].map({"team1": 0, "team2": 1, "draw": 2})

print("Final X shape:", X.shape)
print("Final y shape:", y.shape)