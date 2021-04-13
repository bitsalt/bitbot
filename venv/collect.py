"""
Get stock quote data using yFinance

"""

import datetime as dt
import yfinance as yf
import pandas as pd

tickers = ['BTC-USD', 'EUR-USD', 'USD-CAD']
end = dt.datetime.today()
start = end - dt.timedelta(30)
# closePrice = pd.DataFrame()
data = {}

for ticker in tickers:
    # closePrice[ticker] = yf.download(ticker, start, end)["Adj Close"]
    data[ticker] = yf.download(ticker, start, end)

print(data)