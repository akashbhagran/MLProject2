from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
import mlflow.pyfunc
import os
import sqlite3
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import time
import redis
import os
from mlflow.tracking import MlflowClient
import pickle

redis_host = os.getenv('REDIS_HOST')
r = redis.Redis(host=redis_host, decode_responses=True)

mlflow.set_tracking_uri("http://mlflow:5000")

if __name__ == '__main__':

    client = MlflowClient()
    meta = client.get_latest_versions(name = 'LogRegFruits')
    model_name = meta[0].name
    model_version = meta[0].version
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.pyfunc.load_model(model_uri)
    logreg = model
    scaler = MinMaxScaler()

    #path = 'mlartifacts' + meta[0].source.split(':')[1] + '/model.pkl'
    #scaler = MinMaxScaler()
    
    #with open(path, 'rb') as f:
    #    pickled_model = pickle.load(f)

    #logreg = pickled_model
    scores = []
    iteration = 0

    while(True):

        #if not r.exists('write_lock'):
            
        iteration += 1

        # Get from DB
        conn = sqlite3.connect('data/fruits.db')
        df = pd.read_sql("SELECT * FROM FRUITS", conn)
        conn.close()

        # Define X and y
        X = df[['MASS','WIDTH','HEIGHT','COLOUR']]
        y = df['FRUITLABEL']
        y = np.array(y).astype('int32')
        X = scaler.fit_transform(np.array(X))
        out = logreg.predict(X)
        #score = logreg.score(X, y)

        #scores.append(score)
        print(out, flush = True)

        time.sleep(8)