from datetime import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import plotly as pl
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

msft = data.loc["MSFT"].dropna()
msft = msft["2018-06-01":]

mm_12 = get_ema(12, msft.Close)
mm_26 = get_ema(26, msft.Close)

mm_macd = mm_12.EMA - mm_26.EMA
mm_signal = get_ema(9, mm_macd.dropna()).EMA

msft = msft[mm_signal.index[0]:]

trace_macd = go.Scatter(x=mm_macd.index,
                        y=mm_macd,
                        name="MACD",
                        line=dict(color="#17BECF"),
                        opacity=1)

trace_signal = go.Scatter(x=mm_signal.index,
                          y=mm_signal,
                          name="Signal",
                          line=dict(color="#B22222"),
                          opacity=1)

trace_candles = go.Candlestick(x=msft.index,
                              open=msft.Open,
                              high=msft.High,
                              low=msft.Low,
                              close=msft.Close)

fig = pl.subplots.make_subplots(rows=2, cols=1)
fig.append_trace(trace_candles, 1, 1)
fig.append_trace(trace_macd, 2, 1)
fig.append_trace(trace_signal, 2, 1)
fig["layout"]["yaxis2"].update(range=[-3, 5])
simple_config_plot(fig, "Moving Average Convergence/Divergence")
fig.show()
