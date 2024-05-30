import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from fastapi import FastAPI
from data_process import get_data
import json
from datetime import datetime
import pickle
import mlflow

app = FastAPI()
mlflow.set_tracking_uri("http://mlflow:5000")

d = get_data()
d.transform()
X_train, X_test, y_train,y_test = d.get()

with open("config.json") as f:

    config = json.load(f)

logreg = LogisticRegression(penalty = config['penalty'], fit_intercept=config['fit_intercept'], C = config['C'])
logreg.fit(X_train, y_train)

current_dateTime = datetime.now()
name = "LogRegFruits"

mlflow.set_experiment("Run1")

if __name__ == '__main__':

    with mlflow.start_run():

        mlflow.log_param("test", 0.5)

        mlflow.sklearn.log_model(
            sk_model=logreg,
            artifact_path="LogRegFruits",
            registered_model_name=name,
        )