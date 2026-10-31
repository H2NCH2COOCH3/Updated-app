import pandas as pd
import os

FILE = "data/weight.csv"

def save_weight(day, weight):
    df = pd.DataFrame([[day, weight]], columns=["day", "weight"])
    if not os.path.exists(FILE):
        df.to_csv(FILE, index=False)
    else:
        df.to_csv(FILE, mode="a", header=False, index=False)

def load_weight():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["day", "weight"])
