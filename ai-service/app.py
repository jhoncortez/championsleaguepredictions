# # 3. Python AI Service
# # Key Responsibilities:

# # Machine learning model for predictions

# # Processing recent events data

# # Returning prediction probabilities

# import json
# import pickle
# import numpy as np
# import pandas as pd
# from flask import Flask, request
# import joblib

# app = Flask(__name__) 

# model = joblib.load('model.pkl')

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     features = np.array(data['features'])
#     prediction = model.predict(features)
#     return {'prediction': prediction.tolist()}