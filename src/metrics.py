import numpy as np
import pandas as pd


def compute_simple_returns(prices):
    """
    Compute simple daily returns.
    """
    return prices.pct_change()


def compute_cumulative_returns(simple_returns):
    """
    Convert daily returns into an equity curve.
    """
    return (1 + simple_returns).cumprod()


def compute_volatility(simple_returns):
    """
    Standard deviation of daily returns.
    """
    return simple_returns.std()


def compute_max_drawdown(cumulative_returns):
    """
    Maximum peak-to-trough loss.
    """
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    return drawdown.min()


def moving_average_strategy(prices, window=20):
    """
    Trend-following strategy:
    Invest when price is above moving average.
    """
    moving_avg = prices.rolling(window).mean()
    signal = prices > moving_avg
    position = signal.shift(1).fillna(0)
    return position

def compute_strategy_returns(asset_returns: pd.Series,
                             positions: pd.Series) -> pd.Series:
    """
    Strategy return = position(t-1) * asset_return(t)
    """
    return positions.shift(1) * asset_returns


def equity_curve(returns: pd.Series) -> pd.Series:
    """
    Converts returns into cumulative equity curve
    """
    return (1 + returns.fillna(0)).cumprod()

# Backwards-compatible names expected by scripts that import from `metrics`
simple_returns = compute_simple_returns
volatility = compute_volatility
max_drawdown = compute_max_drawdown