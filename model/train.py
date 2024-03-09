import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from fastapi import FastAPI
from model.data_process import get_data
import json
from datetime import datetime
import pickle

app = FastAPI()

d = get_data()
d.transform()
X_train, X_test, y_train,y_test = d.get()

with open("config.json") as f:

    config = json.load(f)

logreg = LogisticRegression(penalty = config['penalty'], fit_intercept=config['fit_intercept'], C = config['C'])
logreg.fit(X_train, y_train)

current_dateTime = datetime.now()
path = 'C:/Users/akash/Documents/MLProjects/LiveData/ModelRegistry/MLproject2'
model_name = '/LogReg_' + str(current_dateTime).split(".")[0].replace(" ","_").replace(":","_") + '.pkl'

print(path+model_name)

with open(path + model_name, 'wb') as file:
    pickle.dump(logreg, file)

with open(path+model_name, 'rb') as file:
    loaded_model = pickle.load(file)

logreg = loaded_model

@app.get("/")
async def get_accuracy():
    train_accuracy = logreg.score(X_train, y_train)
    test_accuracy = logreg.score(X_test, y_test)
    print()
    return {
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "test_accuracy2": test_accuracy
        }