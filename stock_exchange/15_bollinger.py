from datetime import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import plotly.graph_objs as go


def get(tickers, start_date, end_date):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    datas = map(data, tickers)
    return pd.concat(datas, keys=tickers, names=["ticker", "date"])


def get_ema(window, prices):
    K = (2 / (window + 1))
    ma = prices.rolling(window=window).mean().dropna()

    data = pd.DataFrame(index=ma.index)
    data["Price"] = prices
    data["EMA"] = np.NaN
    data.EMA[0] = ma[1]

    for i in range(1, len(data)):
        data.EMA[i] = (data.Price[i] * K) + ((1 - K) * data.EMA[i - 1])

    return data


def simple_config_plot(fig, title):
    title={"text": title,
           "xanchor": "center",
           "yanchor": "bottom",
           "y": 0,
           "x": 0.5}


def simple_plot(data, title):
    fig = go.Figure(data=data)
    simple_config_plot(fig, title)
    fig.show()


tickers = ["AAPL", "MSFT", "^GSPC"]
start_date = datetime(year=2018, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2019, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)

data = get(tickers, start_date, end_date)
aapl = data.loc["AAPL"]["2018-01-01":"2018-12-31"].dropna()

window = 20
aapl_avg = aapl.Close.rolling(window=window).mean().dropna()
aapl_std = aapl.Close.rolling(window=window).std().dropna()

aapl_bollinger = pd.DataFrame(index=aapl_avg.index)
aapl_bollinger["mband"] = aapl_avg
aapl_bollinger["uband"] = aapl_avg + aapl_std.apply(lambda x: (x * 2))
aapl_bollinger["lband"] = aapl_avg - aapl_std.apply(lambda x: (x * 2))

aapl_prices = aapl[aapl_bollinger.index[0]:]

prices = go.Candlestick(x=aapl_prices.index,
                        open=aapl_prices.Open,
                        high=aapl_prices.High,
                        low=aapl_prices.Low,
                        close=aapl_prices.Close,
                        name="Prices")

uband = go.Scatter(x=aapl_bollinger.index,
                   y=aapl_bollinger.uband,
                   name="Upper Band",
                   line=dict(color="#17BEFC"),
                   opacity=1)

mband = go.Scatter(x=aapl_bollinger.index,
                   y=aapl_bollinger.mband,
                   name="Moving Average",
                   line=dict(color="#B22222"),
                   opacity=1)

lband = go.Scatter(x=aapl_bollinger.index,
                   y=aapl_bollinger.lband,
                   name="Lower Band",
                   line=dict(color="#17BEFC"),
                   opacity=1)

data = [prices, uband, lband, mband]
simple_plot(data, "Bollinger Bands")
