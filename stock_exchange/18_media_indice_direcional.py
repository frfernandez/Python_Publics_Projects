from datetime import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import plotly.graph_objs as go
import plotly.subplots as tools


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


tickers = ["VALE3.SA"]
start_date = datetime(year=2018, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)

data = get(tickers, start_date, end_date).loc["VALE3.SA"].dropna()
data_ant = data.shift(1)

tr = pd.DataFrame([data.High - data.Low,
                   np.absolute(data.High - data_ant.Close),
                   np.absolute(data.Low - data_ant.Close)])
tr = tr.transpose()
tr = tr.max(axis=1)

data["tr"] = tr
print("data[tr]")
print(data)

dm_plus = np.where((data.High - data_ant.High) > (data_ant.Low - data.Low),
                   (data.High - data_ant.High).apply(lambda x: np.max([x, 0])), 0)
dm_minus = np.where((data_ant.Low - data.Low) > (data.High - data_ant.High),
                    (data_ant.Low - data.Low).apply(lambda x: np.max([x, 0])), 0)

data["dmPlus"] = dm_plus
data["dmMinus"] = dm_minus
data = data[1:]
print()
print("data[1:]")
print(data)

window = 14
data["trAvg"] = np.NaN
data["dmPlusAvg"] = np.NaN
data["dmMinusAvg"] = np.NaN

data.trAvg[window - 1] = np.sum(data.iloc[0:window].tr)
data.dmPlusAvg[window - 1] = np.sum(data.iloc[0:window].dmPlus)
data.dmMinusAvg[window - 1] = np.sum(data.iloc[0:window].dmMinus)

for i in range(window, len(data)):
    data.trAvg[i] = data.trAvg[i - 1] - (data.trAvg[i - 1] / window) + data.tr[i]
    data.dmPlusAvg[i] = data.dmPlusAvg[i - 1] - (data.dmPlusAvg[i - 1] / window) + data.dmPlus[i]
    data.dmMinusAvg[i] = data.dmMinusAvg[i - 1] - (data.dmMinusAvg[i - 1] / window) + data.dmMinus[i]

data = data.dropna()
data["diPlus"] = (data.dmPlusAvg / data.trAvg) * 100
data["diMinus"] = (data.dmMinusAvg / data.trAvg) * 100
print()
print("diPlus")
print(data["diPlus"])
print()
print("diMinus")
print(data["diMinus"])

data["DX"] = (np.absolute(data.diPlus - data.diMinus) / (data.diPlus - data.diMinus)) * 100
data["ADX"] = np.NaN
data.ADX[window - 1] = data.DX[0:window].mean()

for i in range(window, len(data)):
    data.ADX[i] = (data.ADX[i - 1] * (window - 1) + data.DX[i]) / window

data = data.dropna()
print()
print("data")
print(data)

trace_di_minus = go.Scatter(x=data.index,
                            y=data.EMA1,
                            name="EMA(1)",
                            line=dict(color="#FF00CF"),
                            opacity=1)

trace_di_plus = go.Scatter(x=data.index,
                           y=data.EMA9,
                           name="EMA(9)",
                           line=dict(color="#17BECF"),
                           opacity=1)

trace_candles = go.Candlestick(x=data.index,
                               open=data.Open,
                               high=data.High,
                               low=data.Low,
                               close=data.Close)

fig = tools.make_subplots(rows=2, cols=1)
fig.append_trace(trace_candles, 1, 1)
fig.append_trace(trace_di_minus, 2, 1)
fig.append_trace(trace_di_plus, 2, 1)
#fig.append_trace(trace_adx, 2, 1)

fig["layout"]["yaxis2"].update(range=[0, 100],
                               showgrid=True,
                               gridwidth=1,
                               gridcolor="WE8E8E8")

fig["layout"]["xaxis2"].update(showgrid=True,
                               gridwidth=1,
                               gridcolor="WE8E8E8")

simple_config_plot(fig, "Média do Índice Direcional")
fig.show()
