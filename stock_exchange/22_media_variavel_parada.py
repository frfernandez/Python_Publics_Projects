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
factor = 2.7
down_trend_buffer = []
up_trend_buffer = []
iter_count = -1

for i, item in df.iterrows():
    iter_count += 1
    if iter_count < atr_period:
        down_trend_buffer.append(0)
        up_trend_buffer.append(0)
        continue
    elif iter_count == atr_period:
        down_trend_buffer.append(item.close + item.atr * factor)
        up_trend_buffer.append(item.close - item.atr * factor)
        continue

    pre_down_trend = item.close + item.atr * factor
    pre_up_trend = item.close - item.atr * factor

    if (item.close_prev > down_trend_buffer[iter_count - 1]) and (down_trend_buffer[iter_count - 1] > 0):
        down_trend_buffer.append(0)
        up_trend_buffer.append(pre_up_trend)
    elif (item.close_prev < up_trend_buffer[iter_count - 1]) and (up_trend_buffer[iter_count - 1] > 0):
        down_trend_buffer.append(pre_down_trend)
        up_trend_buffer.append(0)
    else:
        down_trend_buffer.append(0 if down_trend_buffer[iter_count - 1] == 0
                                   else min(pre_down_trend, down_trend_buffer[iter_count - 1]))
        up_trend_buffer.append(0 if up_trend_buffer[iter_count - 1] == 0
                                 else min(pre_up_trend, up_trend_buffer[iter_count - 1]))

    down_trend = pre_down_trend
    up_trend = pre_up_trend

df = pd.DataFrame(data=dict(open=aapl.Open,
                            high=aapl.High,
                            low=aapl.Low,
                            close=aapl.Close,
                            close_prev=aapl.Close.shift(1)))

df["down_trend"] = down_trend_buffer
df["up_trend"] = up_trend_buffer

df["down_trend"] = np.where(df.down_trend == 0, np.NaN, df.down_trend)
df["up_trend"] = np.where(df.up_trend == 0, np.NaN, df.up_trend)

_data = df

trace_up_trend = go.Scatter(name="ATR - Trend Up",
                            x=_data.index,
                            y=_data.up_trend,
                            line=dict(color="17BECF"),
                            opacity=1)

trace_down_trend = go.Scatter(name="ATR - Trend Down",
                            x=_data.index,
                            y=_data.down_trend,
                            line=dict(color="B22222"),
                            opacity=1)

trace = go.Candlestick(name="AAPL",
                       x=_data.index,
                       open=_data.open,
                       high=_data.high,
                       low=_data.low,
                       close=_data.close)

data = [trace_up_trend, trace_down_trend]

simple_plot(data, "Média Variável Parada")
