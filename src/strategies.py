import pandas as pd


def moving_average_strategy(data: pd.DataFrame, window: int = 3) -> pd.Series:
    ma = data["Close"].rolling(window).mean()
    position = data["Close"] > ma
    return position.astype(int)

import pandas as pd

def moving_average_strategy(data: pd.DataFrame, window: int = 3) -> pd.Series:
    ma = data["Close"].rolling(window).mean()
    position = data["Close"] > ma
    return position.astype(int)
