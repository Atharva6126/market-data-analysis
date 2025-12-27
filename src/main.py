import pandas as pd
import numpy as np

from metrics import (
    simple_returns,
    moving_average_strategy,
    compute_strategy_returns,
    equity_curve,
    volatility,
    max_drawdown
)

# Load data
df = pd.read_csv("data/AAPL.csv")

# Asset returns
df["asset_return"] = simple_returns(df["Close"])

# Strategy signal & position
df["position"] = moving_average_strategy(df["Close"], window=3)

# Strategy returns
df["strategy_return"] = compute_strategy_returns(
    df["asset_return"],
    df["position"]
)

# Equity curves
df["asset_equity"] = equity_curve(df["asset_return"])
df["strategy_equity"] = equity_curve(df["strategy_return"])

# ---- Report ----
print("\nQuant Research Report")
print("---------------------")
print(f"Observations: {len(df)}")
print(f"Asset Volatility: {volatility(df['asset_return']):.4f}")
print(f"Asset Max Drawdown: {max_drawdown(df['asset_equity']):.4f}")

print("\nStrategy Performance")
print("---------------------")
print(f"Strategy Volatility: {volatility(df['strategy_return']):.4f}")
print(f"Strategy Max Drawdown: {max_drawdown(df['strategy_equity']):.4f}")

print("\nFinal Equity Values")
print("-------------------")
print(f"Asset Final Equity: {df['asset_equity'].iloc[-1]:.4f}")
print(f"Strategy Final Equity: {df['strategy_equity'].iloc[-1]:.4f}")
