"""
data.py
This module loads in data.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class get_data():

    def __init__(self, path: str = 'fruit_data_with_colors.txt') -> None:
        fruits = pd.read_table(path)
        feature_names = ['mass', 'width', 'height', 'color_score']
        self.X = fruits[feature_names]
        self.y = fruits['fruit_label']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=0)
        
        
    def transform(self) -> None:
        
        scaler = MinMaxScaler()
        
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def get(self):
        
        return self.X_train, self.X_test, self.y_train, self.y_test