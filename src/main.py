import pandas as pd
from metrics import (
    compute_simple_returns,
    compute_cumulative_returns,
    compute_volatility,
    compute_max_drawdown
)

def main():
    df = pd.read_csv("data/AAPL.csv")

    prices = df["Close"]

    simple_returns = compute_simple_returns(prices)
    cumulative_returns = compute_cumulative_returns(simple_returns)

    volatility = compute_volatility(simple_returns)
    max_dd = compute_max_drawdown(cumulative_returns)

    print("Quant Research Report")
    print("---------------------")
    print(f"Observations: {len(df)}")
    print(f"Volatility: {volatility:.4f}")
    print(f"Max Drawdown: {max_dd:.4f}")

if __name__ == "__main__":
    main()
