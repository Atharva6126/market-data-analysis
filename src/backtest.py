import pandas as pd


def run_backtest(data: pd.DataFrame, position: pd.Series) -> pd.DataFrame:
    data = data.copy()
    data["return"] = data["Close"].pct_change()
    data["strategy_return"] = position.shift(1) * data["return"]
    data["bh_equity"] = (1 + data["return"]).cumprod()
    data["strategy_equity"] = (1 + data["strategy_return"]).cumprod()
    return data

import pandas as pd

def run_backtest(data: pd.DataFrame, position: pd.Series) -> pd.DataFrame:
    data = data.copy()
    data["return"] = data["Close"].pct_change()
    data["strategy_return"] = position.shift(1) * data["return"]
    data["bh_equity"] = (1 + data["return"]).cumprod()
    data["strategy_equity"] = (1 + data["strategy_return"]).cumprod()
    return data
