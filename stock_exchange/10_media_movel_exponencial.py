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
start_date = datetime(year=2018, month=6, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2019, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)
window = 21
K = (2 / (window + 1))

data = get(tickers, start_date, end_date)

msft = data.loc["MSFT"].dropna()
msft = msft["2018-06-01":]
MA = msft.Close.rolling(window=window).mean().dropna()

ema_data = pd.DataFrame(index=MA.index)
ema_data["Price"] = msft.Close
ema_data["MA"] = MA
ema_data["EMA"] = np.NaN

ema_data.EMA[0] = ema_data.MA[1]

for i in range(1, len(ema_data)):
    ema_data.EMA[i] = (ema_data.Price[i] * K) + ((1 - K) * ema_data.EMA[i - 1])

trace_ma = go.Scatter(x=ema_data.index,
                      y=ema_data.MA,
                      name="MSFT MA(21)",
                      line=dict(color="#BEBECF"),
                      opacity=1)

trace_ema = go.Scatter(x=ema_data.index,
                       y=ema_data.EMA,
                       name="MSFT MA(21)",
                       line=dict(color="#17BECF"),
                       opacity=1)

trace_candles = go.Candlestick(x=msft.index,
                               open=msft.Open,
                               high=msft.High,
                               low=msft.Low,
                               close=msft.Close,
                               name="Price")

data = [trace_ma, trace_ema, trace_candles]
simple_plot(data, "Exponential moving average")
