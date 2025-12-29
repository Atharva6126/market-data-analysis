import pandas as pd
from typing import Any


def moving_average_strategy(data: pd.DataFrame, window: Any = 3) -> pd.Series:
    """Return a 0/1 position Series where price > rolling moving average.

    The `window` parameter is validated and coerced to an integer >= 1.
    If an invalid value is passed, a default of 3 is used.
    """
    # Coerce/validate window
    try:
        w = int(window)
    except Exception:
        w = 3
    if w < 1:
        w = 3

    ma = data["Close"].rolling(window=w, min_periods=1).mean()
    position = data["Close"] > ma
    return position.astype(int).reindex(data.index)


def buy_and_hold_strategy(data: pd.DataFrame) -> pd.Series:
    return pd.Series(1, index=data.index)
