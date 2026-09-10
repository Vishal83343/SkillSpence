import pandas as pd
import os

FILE_PATH = "data/expenses.csv"

def initialize_file():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["amount", "category"])
        df.to_csv(FILE_PATH, index=False)

def add_expense(amount, category):
    initialize_file()
    df = pd.read_csv(FILE_PATH)

    new = pd.DataFrame([[amount, category]], columns=["amount", "category"])
    df = pd.concat([df, new], ignore_index=True)

    df.to_csv(FILE_PATH, index=False)

def get_expenses():
    initialize_file()
    return pd.read_csv(FILE_PATH)
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_expense(data):
    if len(data) < 2:
        return None

    # X = time index
    X = np.array(range(len(data))).reshape(-1, 1)
    
    # y = amount
    y = data["amount"].values

    model = LinearRegression()
    model.fit(X, y)

    # predict next point
    next_index = np.array([[len(data)]])
    prediction = model.predict(next_index)

    return int(prediction[0])