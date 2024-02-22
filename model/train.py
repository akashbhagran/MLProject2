import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from fastapi import FastAPI
import uvicorn

import os


# Change the current working directory
os.chdir('./')

app = FastAPI()

fruits = pd.read_table('data/fruit_data_with_colors.txt')

feature_names = ['mass', 'width', 'height', 'color_score']
X = fruits[feature_names]
y = fruits['fruit_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

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