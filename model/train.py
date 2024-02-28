import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from fastapi import FastAPI
from model.data_process import get_data

app = FastAPI()

d = get_data()
d.transform()
X_train, X_test, y_train,y_test = d.get()


logreg = LogisticRegression()
logreg.fit(X_train, y_train)

@app.get("/")
async def get_accuracy():
    train_accuracy = logreg.score(X_train, y_train)
    test_accuracy = logreg.score(X_test, y_test)
    return {
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy
    }