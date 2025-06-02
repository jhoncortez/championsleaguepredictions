import pandas as pd
from calculate_features import calculate_team_form, calculate_head_to_head, calculate_stage_importance, calculate_venue_advantage
from data import get_data_from_json

# import numpy as np

def outcome_result(match):
    if match["score"]["winner"] == "HOME_TEAM":
        return 1
    elif match["score"]["winner"] == "AWAY_TEAM":
        return 2
    else:
        return 0

def create_training_data():

    #### Get data from database or json file
    data = get_data_from_json() 
    matches = data['matches']

    training_data = []
    # outcomes = []
    
    # identify the last season
    seasons = set(match.get('season') for match in matches if 'season' in match)
    last_season = max(seasons) if seasons else None
    
    for match in matches:
        # Skip matches without scores or not from last season
        if (match["score"]["fullTime"]["home"] is None or 
            (last_season and match.get('season') != last_season)):
            continue
            
        match_date = match["utcDate"]
        home_name = match["homeTeam"]["name"]
        away_name = match["awayTeam"]["name"]
        stage = match.get("stage", "GROUP_STAGE")  # Default to "GROUP_STAGE" if stage is not present
        venue = match.get("venue", "HOME")
        
        # Get features
        home_form = calculate_team_form(matches, home_name, match_date)
        away_form = calculate_team_form(matches, away_name, match_date)
        head_to_head_team1_wins , head_to_head_team2_wins = calculate_head_to_head(matches, home_name, away_name, match_date)

        # New features
        stage_importance = calculate_stage_importance(stage)
        venue_advantage = calculate_venue_advantage(venue)  # Home team always has advantage in historical data

    
        # outcomes.append(outcome_result(match))
        
        training_data.append({
            "team1_avg_goals": home_form["avg_goals"],
            "team2_avg_goals": away_form["avg_goals"],
            "team1_win_rate": home_form["win_rate"],
            "team2_win_rate": away_form["win_rate"],
            "head_to_head_team1_wins": head_to_head_team1_wins,
            "head_to_head_team2_wins": head_to_head_team2_wins,
            "home_wins": home_form["wins"], 
            "away_wins": away_form["wins"], 
            "home_losses": home_form["losses"], 
            "away_losses": away_form["losses"], 
            "home_matches": home_form["total_matches"], 
            "away_matches": away_form["total_matches"], 
            "home_advantage": home_form["advantage"], 
            "away_advantage": away_form["advantage"], 
            "home_draws": home_form["draws"], 
            "away_draws": away_form["draws"], 
            "home_goals_conceded": home_form["goals_conceded"],
            "away_goals_conceded": away_form["goals_conceded"],
            "home_goals_scored": home_form["goals_scored"],
            "away_goals_scored": away_form["goals_scored"],
            "home_goal_diff": home_form["goal_diff"],
            "away_goal_diff": away_form["goal_diff"],
            "stage_importance": stage_importance,
            "venue_advantage": venue_advantage,
            "outcome": outcome_result(match)
        })
    
    return  pd.DataFrame(training_data)

