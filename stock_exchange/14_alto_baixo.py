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

window = 8
aapl_high_avg = aapl.High.rolling(window=window).mean()
aapl_low_avg = aapl.Low.rolling(window=window).mean()

trace_high = go.Scatter(x=aapl_high_avg.index,
                        y=aapl_high_avg,
                        name="AAPL High Avg",
                        line=dict(color="#17BEFC"),
                        opacity=1)

trace_low = go.Scatter(x=aapl_low_avg.index,
                       y=aapl_low_avg,
                       name="AAPL Low Avg",
                       line=dict(color="#B22222"),
                       opacity=1)

trace = go.Candlestick(x=aapl.index,
                       open=aapl.Open,
                       high=aapl.High,
                       low=aapl.Low,
                       close=aapl.Close)

data = [trace_high, trace_low, trace]
simple_plot(data, "HiLo Activator - Bands")

aapl_high = pd.DataFrame(index=aapl.index)
aapl_low = pd.DataFrame(index=aapl.index)

aapl_high["high"] = np.where(aapl.Close > aapl_high_avg, aapl_low_avg, np.NaN)
aapl_low["low"] = np.where(aapl.Close < aapl_low_avg, aapl_high_avg, np.NaN)

trace_high = go.Scatter(x=aapl_high.index,
                        y=aapl_high,
                        name="AAPL High Avg",
                        line=dict(color="#17BEFC"),
                        opacity=1)

trace_low = go.Scatter(x=aapl_low.index,
                       y=aapl_low,
                       name="AAPL Low Avg",
                       line=dict(color="#B22222"),
                       opacity=1)

trace = go.Candlestick(x=aapl.index,
                       open=aapl.Open,
                       high=aapl.High,
                       low=aapl.Low,
                       close=aapl.Close)

data = [trace_high, trace_low, trace]
simple_plot(data, "HiLo Activator")
