from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from fastapi import FastAPI
import os
import sqlite3
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import mlflow
import time

app = FastAPI()

mlflow.set_tracking_uri(uri="http://127.0.0.1:8095")
mlflow.set_experiment("Run1")

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

def log_chart(scores, iteration):
    """Generate and log a chart of scores."""
    plt.figure(figsize=(10,6))
    plt.plot(scores, label="LogReg Score", marker='o')
    plt.xlabel("Iteration")
    plt.ylabel("Score")
    plt.title(f"LogReg Score Over Time - Iteration {iteration}")
    plt.legend()
    plt.savefig("score_chart1.png")
    plt.close()
    # Log the chart as an artifact
    mlflow.log_artifact("score_chart1.png", artifact_path="charts")

if __name__ == '__main__':
    
    scores = []
    iteration = 0

    with mlflow.start_run() as run:

        while(1):

            iteration += 1

            # Get from DB
            conn = sqlite3.connect('C:/Users/akash/Documents/MLProjects/MLproject2/simulate/fruits.db')
            df = pd.read_sql("SELECT * FROM FRUITS", conn)
            conn.close()

            # Define X and y
            X = df[['MASS','WIDTH','HEIGHT','COLOUR']]
            y = df['FRUITLABEL']
            y = np.array(y).astype('int32')
            X = scaler.fit_transform(np.array(X))
            out = logreg.predict(X)
            score = logreg.score(X, y)

            scores.append(score)

            if iteration % 10 == 0:
                log_chart(scores, run.info.run_id)

            mlflow.log_metric("score",score)

            time.sleep(5)