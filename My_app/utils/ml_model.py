from sklearn.linear_model import LinearRegression
import numpy as np

def load_sleep_model():
    x = np.array([
        [10, 1, 8],
        [20, 5, 6],
        [25, 8, 3],
        [30, 6, 5],
        [35, 2, 9],
        [40, 4, 3]
    ])
    y = np.array([10, 8, 6, 7, 9.5, 9])

    model = LinearRegression()
    model.fit(x, y)
    return model
