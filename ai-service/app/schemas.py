from pydantic import BaseModel
from typing import Optional, List

class Player(BaseModel):
    id: int
    name: str
    position: str
    dateOfBirth: str
    nationality: str
    current_rating: Optional[float] = None

class Coach(BaseModel):
    id: int
    name: str
    dateOfBirth: str
    nationality: str
    cl_titles: Optional[int] = 0
    
class TeamInfo(BaseModel):
    id: int
    name: str
    shortName: str
    tla: str
    crest: str
    founded: int
    venue: str
    coach: Coach
    squad: List[Player]
    league_level: Optional[float] = None  # Tier 1-4

class MatchPredictionRequest(BaseModel):
    team1: str
    team2: str
    venue: Optional[str] = "HOME"  # HOME or AWAY for team1
    stage: Optional[str] = None  # FINAL, SEMI_FINALS, etc.
    team1_injuries: Optional[List[str]] = None
    team2_injuries: Optional[List[str]] = None