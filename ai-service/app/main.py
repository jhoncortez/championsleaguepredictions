from fastapi import FastAPI
from model import predict_match
from schemas import MatchPredictionRequest

app = FastAPI()

@app.post("/predict")
async def predict(match_request: MatchPredictionRequest):
    """Takes team data and returns AI prediction"""
    # print(match_request)
    # print(match_request.dict())
    # # sample data
    # prediction = {
    #     "team1_win": 0.5,
    #     "team2_win": 0.5,
    #     "draw": 0.0
    # }
    prediction = predict_match(**match_request.dict()) # ** unpacks the dictionary
    # prediction = predict_match_outcome(
    #     team1=match_request.team1,
    #     team2=match_request.team2,
    #     team1_form=match_request.team1_form,
    #     team2_form=match_request.team2_form,
    #     head_to_head=match_request.head_to_head,
    #     injuries=match_request.injuries
    # )
    return {"prediction": prediction}