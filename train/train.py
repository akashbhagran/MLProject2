import pandas as pd
from sklearn.linear_model import LogisticRegression
from data_process import get_data
import json
from datetime import datetime
import mlflow
from mlflow.models import infer_signature
import pickle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

mlflow.set_tracking_uri("http://localhost:5000")

d = get_data()
d.transform()
X_train, X_test, y_train,y_test = d.get()

with open("config.json") as f:

    config = json.load(f)

logreg = LogisticRegression(penalty = config['penalty'], fit_intercept=config['fit_intercept'], C = config['C'])
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

pickle.dump(logreg, open('model.sav', 'wb'))
logreg = pickle.load(open('model.sav', 'rb'))

acc = logreg.score(X_test,y_test)
with open("metrics.txt", "w") as outfile:
    outfile.write("Accuracy: " + str(acc))

cm = confusion_matrix(y_test,y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm).plot()
disp.figure_.savefig('confusion_matrix.png')

current_dateTime = datetime.now()
name = "LogRegFruits"
mlflow.set_experiment("Run1")
signature = infer_signature(X_train, logreg.predict(X_train))

if __name__ == '__main__':

    with mlflow.start_run():

        mlflow.log_param("test", 0.5)

        mlflow.sklearn.log_model(
            sk_model=logreg,
            artifact_path="LogRegFruits",
            registered_model_name=name,
            signature = signature
        )