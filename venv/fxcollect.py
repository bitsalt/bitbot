"""
Get ForEx and/or stock data

"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time


tickers = ['EURUSD', 'USDCAD', 'USDCHF', 'AUDUSD', 'NZDUSD']
forex_data = pd.DataFrame()
api_call_count = 0


for ticker in tickers:
    start_time = time.time()
    ts = TimeSeries(key='G07RKXPZQB3GXC5J', output_format='pandas', indexing_type='integer')
    data, meta_data = ts.get_intraday(symbol=ticker, interval='15min', outputsize='compact')
    api_call_count += 1
    data.columns = ['index', 'open', 'high', 'low', 'close', 'volume']

    # reverse the order...at least for this course. I think ultimately, having the latest data
    # first makes better sense. But the course backtesting assumes chronological order
    forex_data = forex_data.iloc[::1]

    forex_data[ticker] = data['close']

    # This is more useful if there are more than 5 ticker symbols
    # ...or perhaps if it's going to be continuously run during the trading day.
    if api_call_count > 5:
        api_call_count = 0
        time.sleep(61 - (time.time() - start_time))

print(forex_data)
# print(meta_data)
