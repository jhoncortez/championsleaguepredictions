from calculate_features import calculate_team_form, calculate_head_to_head, calculate_stage_importance, calculate_venue_advantage, calculate_injury_impact

from data import get_data_from_json

import pandas as pd

def prepare_prediction_data(team1_name, team2_name, venue="HOME", stage=None, team1_injuries=None, team2_injuries=None):

    #### Get data from database or json file
    data = get_data_from_json() 
    matches = data['matches']

    # Get team form
    home_form = calculate_team_form(matches, team1_name)
    away_form = calculate_team_form(matches, team2_name)
    head_to_head_team1_wins, head_to_head_team2_wins = calculate_head_to_head(matches, team1_name, team2_name)

    # New features
    stage_importance = calculate_stage_importance(stage) if stage else 0.5 # default GROUPS_STAGE
    venue_advantage = calculate_venue_advantage(venue)
    # team1_injury_impact = calculate_injury_impact(team1_injuries or [])
    # team2_injury_impact = calculate_injury_impact(team2_injuries or [])
    
    # Get injuries
    # team1_injuries = get_team_injuries(team1_name)
    
    return pd.DataFrame([{
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
        # "team1_injury_impact": team1_injury_impact,
        # "team2_injury_impact": team2_injury_impact
    }])


# # Example: Predict Real Madrid vs Man City
# team1_id = 'Paris Saint Germain'  # Real Madrid
# team2_id = 'Inter Milan'  # Man City
# # match_date = "2023-05-09T19:00:00Z"

# # Prepare features
# features = prepare_prediction_data(matches, team1_id, team2_id)

# # Make prediction
# prediction = model.predict_proba(pd.DataFrame([features]))[0]
# print(f"Real Madrid win: {prediction[1]:.1%}")
# print(f"Man City win: {prediction[2]:.1%}")
# print(f"Draw: {prediction[0]:.1%}")