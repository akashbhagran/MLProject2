import pytest
import os
import sys
import numpy as np

PATH = os.getcwd() + "/model"

print(PATH)

sys.path.append(PATH)

from data_process import get_data

def test_data_process():

    d = get_data()
    d.transform()
    X_train, X_test, y_train,y_test = d.get()

    assert isinstance(X_train[0][0], np.float64)

