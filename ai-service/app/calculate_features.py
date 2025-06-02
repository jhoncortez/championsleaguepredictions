# import numpy as np
# def calculate_team_form(matches, team_name):
#     form = ""
#     for match in matches:
#         if match["homeTeam"]["name"] == team_name:
#             form += "W" if match["score"]["winner"] == "HOME_TEAM" else "L"
#         elif match["awayTeam"]["name"] == team_name:
#             form += "W" if match["score"]["winner"] == "AWAY_TEAM" else "L"
#         else:
#             form += "D"
#     return form

# def calculate_head_to_head(matches, team1, team2):
#     head_to_head = []
#     # winner = None
#     # head_to_head_team1_wins = 0
#     # head_to_head_team2_wins = 0
#     for match in matches:
#         if (match["homeTeam"]["name"] == team1 and match["awayTeam"]["name"] == team2) or (match["homeTeam"]["name"] == team2 and match["awayTeam"]["name"] == team1):
#             head_to_head.append(match)
#             # if match["score"]["winner"] == "HOME_TEAM":
#             #     winner = team1
#             #     head_to_head_team1_wins += 1
#             # elif match["score"]["winner"] == "AWAY_TEAM":
#             #     winner = team2
#             #     head_to_head_team2_wins += 1
#     return head_to_head

# def calculate_injuries(matches, team_name):
#     injuries = {}
#     for match in matches:
#         if match["homeTeam"]["name"] == team_name:
#             injuries[match["homeTeam"]["name"]] = match["injuries"]
#         elif match["awayTeam"]["name"] == team_name:
#             injuries[match["awayTeam"]["name"]] = match["injuries"]
#     return injuries

# def calculate_avg_goals(matches, team_name):
#     goals = [goal for match in matches 
#              for goal in [match["score"]["fullTime"]["home"] if match["homeTeam"]["name"] == team_name else match["score"]["fullTime"]["away"] if match["awayTeam"]["name"] == team_name else None] 
#              if goal is not None]
#     return np.mean(goals) if goals else 0

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

import datetime


# format 2025-04-16T19:00:00Z
current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
# current_date = datetime.datetime.now()
print(current_date)

def get_team_alls_seasons_matches(matches, team_name, match_date):
    team_matches = []
    for match in matches:
        # print('home', match["homeTeam"]["name"])
        if match["homeTeam"]["name"] == team_name or match["awayTeam"]["name"] == team_name and (not match_date or match['utcDate'] < match_date):
            team_matches.append(match)
    return team_matches

def get_team_last_season_matches(matches, team_name, match_date):
    """Filter matches to only include those from the most recent season"""
    # First, find all unique seasons in the data
    seasons = set()
    for match in matches:
        if 'season' in match:
            seasons.add(match['season'])
    
    if not seasons:
        return []  # No season data available
    
    # Get the most recent season
    last_season = max(seasons)
    
    # Filter matches for this team in the last season
    team_matches = []
    for match in matches:
        if match.get('season') == last_season:
            if (match["homeTeam"]["name"] == team_name or match["awayTeam"]["name"] == team_name) and ( not match_date or match['utcDate'] < match_date):
                team_matches.append(match)
    
    return team_matches

def calculate_team_form(matches, team_name, match_date=current_date):
    team_matches = get_team_last_season_matches(matches, team_name, match_date)

    # Sort by date and take last 5
    last_5 = sorted(team_matches, key=lambda x: x["utcDate"], reverse=True)[:5]

    # print('Number of matches', len(last_5))

    # print(team_matches)
    if not last_5:
        return {"avg_goals": 0, "win_rate": 0, "wins": 0, "losses": 0, "total_matches": 0, "advantage": 0, "draws": 0, "goals_conceded": 0, "goals_scored": 0, "goal_diff": 0}
    
    goals = 0
    goals_conceded = 0
    wins = 0
    losses = 0
    draws = 0
    # form = ""
    for match in last_5:
        print('{} vs {} winner: {}'.format(match["homeTeam"]["name"], match["awayTeam"]["name"], match["score"]["winner"]))
        draws += match["score"]["winner"] == "DRAW"
        if match["homeTeam"]["name"] == team_name:
            goals += match["score"]["fullTime"]["home"] or 0
            goals_conceded += match["score"]["fullTime"]["away"] or 0
            wins += match["score"]["winner"] == "HOME_TEAM"
            losses += match["score"]["winner"] == "AWAY_TEAM"
        elif match["awayTeam"]["name"] == team_name:
            goals += match["score"]["fullTime"]["away"] or 0
            goals_conceded += match["score"]["fullTime"]["home"] or 0
            wins += match["score"]["winner"] == "AWAY_TEAM"
            losses += match["score"]["winner"] == "HOME_TEAM"
    
    form = {
        "avg_goals": goals / len(last_5), 
        "win_rate": wins / len(last_5), 
        "wins": wins, 
        "losses": losses, 
        "total_matches": len(last_5), 
        "advantage": wins / len(last_5) - losses / len(last_5), 
        "draws": draws, 
        "goals_conceded": goals_conceded,
        "goals_scored": goals,
        "goal_diff": goals - goals_conceded
    }
    return form

def get_historical_h2h_matches(matches, team1, team2, match_date):
    head_to_head = []
    for match in matches:
        if (match["homeTeam"]["name"] == team1 and match["awayTeam"]["name"] == team2) or (match["homeTeam"]["name"] == team2 and match["awayTeam"]["name"] == team1) and ( not match_date or match['utcDate'] < match_date):
            head_to_head.append(match)
    return head_to_head

def calculate_head_to_head(matches, team1, team2, match_date=current_date):
    head_to_head = get_historical_h2h_matches(matches, team1, team2, match_date)
    head_to_head_team1_wins = sum(1 for x in head_to_head if x["score"]["winner"] == "HOME_TEAM")
    head_to_head_team2_wins = sum(1 for x in head_to_head if x["score"]["winner"] == "AWAY_TEAM")
    return head_to_head_team1_wins , head_to_head_team2_wins

# calculate_features.py

def calculate_stage_importance(stage):
    """Convert stage to importance weight (0-1)"""
    stage_weights = {
        'FINAL': 1.0,
        'SEMI_FINALS': 0.9,
        'QUARTER_FINALS': 0.8,
        'LAST_16': 0.7,
        'GROUP_STAGE': 0.5,
        'QUALIFICATION': 0.3
    }
    return stage_weights.get(stage, 0.5)

def calculate_venue_advantage(venue):
    """Home advantage factor"""
    return 1.0 if venue == "HOME" else 0.0

def calculate_injury_impact(injured_players, key_players=None):
    """
    Calculate injury impact based on number and importance of injured players
    key_players could be a list of important players for each team
    """
    if not injured_players:
        return 0.0
    
    base_impact = len(injured_players) * 0.05  # 5% per injured player
    
    if key_players:
        key_injuries = len(set(injured_players) & set(key_players))
        base_impact += key_injuries * 0.1  # Extra 10% for key players
        
    return min(base_impact, 0.3)  # Cap at 30% impact