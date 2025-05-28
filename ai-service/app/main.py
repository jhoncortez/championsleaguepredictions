# FastApi endpoit
from fastapi import FastAPI
from model import predict_match_outcome

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



"""Takes team data and returns AI prediction"""
@app.get("/predict")
async def predict():
    return {"message": "prediction to do"}