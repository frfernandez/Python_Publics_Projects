from datetime import datetime
import pandas as pd
import pandas_datareader.data as pdr
import numpy as np


def get(tickers, start_date, end_date):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    datas = map(data, tickers)
    return pd.concat(datas, keys=tickers, names=["ticker", "date"])


tickers = ["AAPL", "MSFT", "^GSPC"]
start_date = datetime(year=2016, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)
weekdays = pd.date_range(start=start_date, end=end_date, freq="B")

data = get(tickers, start_date, end_date)
data = data.reset_index()
data = data.set_index(["date", "ticker"]).sort_index()

close = data["Close"]
close = close.reindex(pd.MultiIndex.from_product([weekdays, tickers], names=["date", "ticker"]), fill_value=np.NaN)
print("close.head(10)")
print(close.head(10))

close = close.reset_index().pivot(index="date", columns="ticker", values="Close")
print()
print("close.describe()")
print(close.describe())
