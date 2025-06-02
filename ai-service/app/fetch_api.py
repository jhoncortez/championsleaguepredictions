# Add this to your data processing script
import requests
import json
import env

#get apikey from .env
# Add your Football Data API token
API_TOKEN = env("API_TOKEN")
HEADERS = {"X-Auth-Token": API_TOKEN}
def fetch_multiple_seasons():
    seasons = ["2023", "2024"]
    all_matches = []
    
    for season in seasons:
        data = requests.get(f"https://api.football-data.org/v4/competitions/CL/matches?season={season[:4]}",
                          headers=HEADERS).json()
        for match in data["matches"]:
            match["season"] = season  # Add season identifier
        all_matches.extend(data["matches"])
    with open("cl-data-3seasons.json", "w") as f:
        json.dump({"matches": all_matches}, f)

def get_team_info(team_id: int) -> Dict:
    """Fetch team data including squad and coach"""
    url = f"http://api.football-data.org/v4/teams/{team_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_competition_top_scores(competition_id: int, season: str) -> Dict:
    url = f"curl -X GET http://api.football-data.org/v4/competitions/{competition_id}/scorers?season={season}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

fetch_multiple_seasons()
# get_competition_top_scores(2000, "2023")