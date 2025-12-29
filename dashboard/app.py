import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Ensure project root is on sys.path so `src` package can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.strategies import moving_average_strategy
from src.backtest import run_backtest
from src.metrics import volatility, max_drawdown

st.title("Quant Research Dashboard")

data = pd.read_csv("data/AAPL.csv")

position = moving_average_strategy(data, window=3)
bt = run_backtest(data, position)

fig, ax = plt.subplots()
ax.plot(bt["Date"], bt["bh_equity"], label="Buy & Hold")
ax.plot(bt["Date"], bt["strategy_equity"], label="Strategy")
ax.legend()
ax.set_title("Equity Curves")
st.pyplot(fig)

st.subheader("Metrics")

st.write("Buy & Hold Volatility:", volatility(bt["return"]))
st.write("Strategy Volatility:", volatility(bt["strategy_return"]))
st.write("Buy & Hold Max Drawdown:", max_drawdown(bt["bh_equity"]))
st.write("Strategy Max Drawdown:", max_drawdown(bt["strategy_equity"]))
