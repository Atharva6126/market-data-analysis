import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("Quant Research Dashboard")

# Load data
data = pd.read_csv("data/AAPL.csv")

# Buy & Hold equity curve
data["return"] = data["Close"].pct_change()
data["equity"] = (1 + data["return"]).cumprod()

# Plot
fig, ax = plt.subplots()
ax.plot(data["Date"], data["equity"])
ax.set_title("Buy & Hold Equity Curve")
ax.set_xlabel("Date")
ax.set_ylabel("Equity")

st.pyplot(fig)
