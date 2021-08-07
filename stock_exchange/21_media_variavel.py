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
aapl = data.loc["AAPL"]["2018-06-01":"2019-02-22"].dropna()

df = pd.DataFrame(data=dict(open=aapl.Open,
                            high=aapl.High,
                            low=aapl.Low,
                            close=aapl.Close,
                            close_prev=aapl.Close.shift(1)))
df["tr"] = df[["high", "close_prev"]].max(axis=1) - df[["high", "close_prev"]].min(axis=1)

atr_period = 21
first_atr = df.tr[atr_period].sum() / atr_period
atr = first_atr
iter_count = 0

atr_list = []
for i, item in df.iterrows():
    if iter_count < atr_period - 1:
        iter_count += 1
        atr_list.append(0)
        continue

    atr = (atr * (atr_period - 1) + item.tr) / atr_period
    atr_list.append(atr)

df["atr"] = atr_list

data = go.Scatter(x=df.index,
                  y=df.atr,
                  opacity=1)

simple_plot(data, "Média Variável")
