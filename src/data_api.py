import logging
import yfinance as yf
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def fetch_stock_data(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch stock data from Yahoo Finance with a local-CSV fallback.

    Attempts to download via yfinance; if it fails or returns empty data,
    falls back to loading `data/{ticker}.csv` from the project root.
    """
    # Prefer local CSV if available (avoids remote download/SSL issues)
    csv_path = Path(__file__).resolve().parents[1] / "data" / f"{ticker}.csv"
    if csv_path.exists():
        logger.info("Loading local CSV for %s: %s", ticker, csv_path)
        data = pd.read_csv(csv_path)
    else:
        try:
            data = yf.download(
                tickers=ticker,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False
            )
        except Exception as e:
            logger.warning("yfinance download failed: %s", e)
            data = pd.DataFrame()

        # If yfinance returned no data, raise
        if data is None or data.empty:
            raise ValueError(f"No data returned for ticker {ticker} and no local CSV found at {csv_path}")

    # Ensure Date is a column (yfinance returns index)
    if isinstance(data.index, pd.DatetimeIndex) and "Date" not in data.columns:
        data = data.reset_index()

    return data
