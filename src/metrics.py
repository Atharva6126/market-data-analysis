import numpy as np

def compute_simple_returns(prices):
    return prices.pct_change()

def compute_cumulative_returns(simple_returns):
    return (1 + simple_returns).cumprod()

def compute_volatility(simple_returns):
    return simple_returns.std()

def compute_max_drawdown(cumulative_returns):
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    return drawdown.min()
