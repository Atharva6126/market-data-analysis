import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import matplotlib.pyplot as plt

from src.data_api import fetch_stock_data
from src.strategies import (
    moving_average_strategy,
    buy_and_hold_strategy
)
from src.backtest import run_backtest
from src.metrics import volatility, max_drawdown

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="Live Quant Dashboard", layout="wide")
st.title("Live Quant Research Dashboard")

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("Market Controls")

ticker = st.sidebar.selectbox(
    "Select Stock",
    {
        "Apple (AAPL)": "AAPL",
        "Google (GOOG)": "GOOG",
        "Microsoft (MSFT)": "MSFT",
    }.items(),
    format_func=lambda x: x[0]
)[1]

strategy_name = st.sidebar.selectbox(
    "Select Strategy",
    ["Buy & Hold", "Moving Average"]
)

ma_window = None
if strategy_name == "Moving Average":
    ma_window = st.sidebar.slider(
        "Moving Average Window",
        5, 50, 20
    )

refresh = st.sidebar.button("Refresh Data")

# -------------------------
# Data loading (cached)
# -------------------------
@st.cache_data(ttl=60)
def load_data(ticker):
    return fetch_stock_data(ticker)

try:
    data = load_data(ticker)
except Exception as e:
    st.error(f"Failed to load data for {ticker}: {e}")
    # Fall back to AAPL local CSV if available
    try:
        data = load_data('AAPL')
        st.warning("Falling back to AAPL local data")
    except Exception:
        st.stop()

# -------------------------
# Strategy selection
# -------------------------
if strategy_name == "Buy & Hold":
    position = buy_and_hold_strategy(data)
else:
    position = moving_average_strategy(data, ma_window)

bt = run_backtest(data, position)

# -------------------------
# Layout
# -------------------------
left_col, right_col = st.columns([3, 1])

# -------------------------
# Plot
# -------------------------
with left_col:
    fig, ax = plt.subplots()

    ax.plot(bt["Date"], bt["bh_equity"], label="Buy & Hold", linestyle="--")

    if strategy_name != "Buy & Hold":
        ax.plot(bt["Date"], bt["strategy_equity"], label=strategy_name)

    ax.set_title(f"{ticker} Equity Curves")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.legend()

    st.pyplot(fig)

# -------------------------
# Metrics
# -------------------------
with right_col:
    st.subheader("Performance Metrics")

    st.metric("Volatility", f"{volatility(bt['strategy_return']):.4f}")
    st.metric("Max Drawdown", f"{max_drawdown(bt['strategy_equity']):.2%}")
