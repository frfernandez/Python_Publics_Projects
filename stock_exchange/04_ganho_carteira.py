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
data = data.reset_index()
data = data.set_index(["date", "ticker"]).sort_index()

daily_close_px = data["Adj Close"].reset_index().pivot("date", "ticker", "Adj Close")
cart_pct_change = daily_close_px / daily_close_px.shift(1) - 1
cart_return = (1 + cart_pct_change).cumprod()
print("cart_return.head(10)")
print(cart_return.head(10))

final_return = cart_return[-1:].apply(lambda x: (x - 1) * 100)
print()
print("final_return")
print(final_return)
