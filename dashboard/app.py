import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.strategies import moving_average_strategy
from src.backtest import run_backtest
from src.metrics import volatility, max_drawdown

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Quant Research Dashboard", layout="wide")

st.title("Quant Research Dashboard")

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Strategy Controls")

ma_window = st.sidebar.slider(
    "Moving Average Window",
    min_value=2,
    max_value=20,
    value=3,
    step=1
)

# -----------------------------
# Load Data
# -----------------------------
data = pd.read_csv("data/AAPL.csv")

# -----------------------------
# Run Strategy + Backtest
# -----------------------------
position = moving_average_strategy(data, window=ma_window)
bt = run_backtest(data, position)

# -----------------------------
# Layout
# -----------------------------
left_col, right_col = st.columns([3, 1])

# -----------------------------
# Equity Curve Plot
# -----------------------------
with left_col:
    fig, ax = plt.subplots()
    ax.plot(bt["Date"], bt["bh_equity"], label="Buy & Hold")
    ax.plot(bt["Date"], bt["strategy_equity"], label="Strategy")
    ax.legend()
    ax.set_title("Equity Curves")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")

    st.pyplot(fig)

# -----------------------------
# Metrics Panel
# -----------------------------
with right_col:
    st.subheader("Performance Metrics")

    st.metric(
        "Buy & Hold Volatility",
        f"{volatility(bt['return']):.4f}"
    )

    st.metric(
        "Strategy Volatility",
        f"{volatility(bt['strategy_return']):.4f}"
    )

    st.metric(
        "Buy & Hold Max Drawdown",
        f"{max_drawdown(bt['bh_equity']):.2%}"
    )

    st.metric(
        "Strategy Max Drawdown",
        f"{max_drawdown(bt['strategy_equity']):.2%}"
    )
