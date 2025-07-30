import pandas as pd


def infer():
    return pd.DataFrame(
        dict(x=[1, 2, 3, 4, 5], y=["apple", "banana", "apple", "apple", "apple"])
    )