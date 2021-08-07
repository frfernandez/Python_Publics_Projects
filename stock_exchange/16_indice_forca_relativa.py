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

window = 14
ifr = pd.DataFrame(index=aapl.index)

ifr_changes = aapl.Close - aapl.Open
ifr["gain"] = ifr_changes[ifr_changes > 0]
ifr["loss"] = ifr_changes[ifr_changes < 0] * (-1)
ifr["gainAVG"] = np.NaN
ifr["lossAVG"] = np.NaN

ifr.gainAVG[window] = ifr.iloc[0:window].gain.mean()
ifr.lossAVG[window] = ifr.iloc[0:window].loss.mean()

for i in range(1, len(ifr)):
    ifr.gainAVG[i] * (ifr.gainAVG[i - 1] * (window - 1) + ifr.gain[i]) / window
    ifr.lossAVG[i] * (ifr.lossAVG[i - 1] * (window - 1) + ifr.loss[i]) / window

ifr["value"] = 100 - (100 / (1 + (ifr.gainAVG / ifr.lossAVG)))

trace_ifr = go.Scatter(x=ifr.index,
                       y=ifr.value,
                       xaxis="x2",
                       yaxis="y2")

trace_candles = go.Candlestick(x=aapl.index,
                               open=aapl.Open,
                               high=aapl.High,
                               low=aapl.Low,
                               close=aapl.Close)

data = [trace_ifr, trace_candles]

layout = go.Layout(xaxis=dict(domain=[0, 1],
                              rangeslider={"visible":False},),
                   yaxis=dict(domain=[0.75, 1],),
                   xaxis2=dict(domain=[0, 1],
                               anchor="y2",
                               showgrid=True,
                               gridwidth=1,
                               gridcolor="#E8E8E8",),
                   yaxis2=dict(domain=[0, 0.45],
                               anchor="x2",
                               range=[0, 100],
                               showgrid=True,
                               gridwidth=1,
                               gridcolor = "#E8E8E8",),
                   shapes=[{"xref":"x2",
                            "yref":"y2",
                            "type":"line",
                            "x0":aapl.index[0],
                            "y0":"20",
                            "x1":aapl.index[-1],
                            "y1":"20",
                            "line":{"color":"rgb(50, 171, 96)",
                                    "width":2,
                                    "dash":"dashdot",},},
                            {"xref":"x2",
                             "yref":"y2",
                             "type":"line",
                             "x0":aapl.index[0],
                             "y0":"70",
                             "x1":aapl.index[-1],
                             "y1":"70",
                             "line":{"color":"rgb(50, 171, 96)",
                                     "width":2,
                                     "dash":"dashdot"},},
                          ])

fig = go.Figure(data=data, layout=layout)
simple_config_plot(fig, "Índice de Força Relativa")
fig.show()
