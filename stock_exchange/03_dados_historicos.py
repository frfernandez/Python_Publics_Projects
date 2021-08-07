from datetime import datetime
import pandas as pd
import pandas_datareader.data as pdr


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
data = get(tickers, start_date, end_date)

print("data.head(10)")
print(data.head(10))

print()
print("data.tail(10)")
print(data.tail(10))