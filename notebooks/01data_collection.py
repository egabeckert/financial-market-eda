# %%
import yfinance as yf
import pandas as pd
import os
# %%

# %%
tickers = [
    'SPY',   # S&P 500 ETF
    'QQQ',   # Nasdaq ETF
    'GLD',   # Gold ETF
    'TLT',   # Long-term Treasury ETF
    'AAPL',  # Tech
    'JPM',   # Finance
    'XOM',   # Energy
    'JNJ',   # Healthcare
]

raw_data = yf.download(
    tickers,
    start='2021-09-07',
    end='2026-09-04',
    interval='1d',
    auto_adjust=False
)
# %%
raw_close = raw_data['Close']
adj_close = raw_data['Adj Close']
# %%
raw_close.head()
# %%
adj_close.head()
# %%
os.getcwd()
# %%
adj_close.to_csv('data/adjusted_close_data.csv')
raw_close.to_csv('data/raw_close_data.csv')
# %%
test_read = pd.read_csv('data/adjusted_close_data.csv')
test_read.info()
# %%
test_read = pd.read_csv('data/adjusted_close_data.csv', index_col=0, parse_dates=True)
test_read.info()
