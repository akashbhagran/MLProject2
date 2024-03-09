from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle
from fastapi import FastAPI
import os
import sqlite3
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = FastAPI()

### Load latest model
path = 'C:/Users/akash/Documents/MLProjects/LiveData/ModelRegistry/MLproject2/'
pkl_files = [file for file in os.listdir(path) if file.endswith('.pkl')]
# Sort the list of files by modification time (latest first)
pkl_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
# Load the latest .pkl file
latest_pkl_file = pkl_files[0]
with open(path+latest_pkl_file, 'rb') as file:
    loaded_model = pickle.load(file)
logreg = loaded_model

scaler = MinMaxScaler()

@app.get("/")
async def run():

    while(1):

        # Get from DB
        conn = sqlite3.connect('C:/Users/akash/Documents/MLProjects/MLproject2/simulate/fruits.db')
        df = pd.read_sql("SELECT * FROM FRUITS", conn)
        conn.close()

        # Define X and y
        X = df[['MASS','WIDTH','HEIGHT','COLOUR']]
        y = df['FRUIT']

        X = scaler.fit_transform(np.array(X))

        out = logreg.predict(X)
        score = logreg.score(X, y)

        return out.tolist(), score
