import pandas as pd
from metrics import (
    compute_simple_returns,
    compute_cumulative_returns,
    compute_volatility,
    compute_max_drawdown,
    moving_average_strategy
)


def main():
    # Load data
    df = pd.read_csv("data/AAPL.csv")

    prices = df["Close"]

    # --- Buy & Hold ---
    simple_returns = compute_simple_returns(prices)
    cumulative_returns = compute_cumulative_returns(simple_returns)

    asset_vol = compute_volatility(simple_returns)
    asset_dd = compute_max_drawdown(cumulative_returns)

    print("Quant Research Report")
    print("---------------------")
    print(f"Observations: {len(df)}")
    print(f"Asset Volatility: {asset_vol:.4f}")
    print(f"Asset Max Drawdown: {asset_dd:.4f}")

    # --- Moving Average Strategy ---
    position = moving_average_strategy(prices)
    strategy_returns = position * simple_returns
    strategy_cumulative = (1 + strategy_returns).cumprod()

    strategy_vol = compute_volatility(strategy_returns)
    strategy_dd = compute_max_drawdown(strategy_cumulative)

    print("\nMoving Average Strategy")
    print("-----------------------")
    print(f"Strategy Volatility: {strategy_vol:.4f}")
    print(f"Strategy Max Drawdown: {strategy_dd:.4f}")


if __name__ == "__main__":
    main()
