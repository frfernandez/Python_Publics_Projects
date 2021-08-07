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


tickers = ["VALE3.SA"]
start_date = datetime(year=2018, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=6, day=28,
                    hour=0, minute=0, second=0, microsecond=0)

data = get(tickers, start_date, end_date)
vale3 = data.loc["VALE3.SA"].dropna()
vale3["EMA1"] = get_ema(1, vale3.Close).EMA
vale3["EMA9"] = get_ema(9, vale3.Close).EMA

buy_cross = (vale3.shift(1).EMA1 < vale3.shift(1).EMA9) & (vale3.EMA1 > vale3.shift(1).EMA9)
sell_cross = (vale3.shift(1).EMA1 > vale3.shift(1).EMA9) & (vale3.EMA1 < vale3.shift(1).EMA9)

vale3["mark_max"] = np.where((vale3.EMA9 < vale3.High) & (vale3.EMA9 > vale3.Low) & (buy_cross == True), vale3.High, 0)
vale3["mark_min"] = np.where((vale3.EMA9 > vale3.Low) & (vale3.EMA9 < vale3.High) & (sell_cross == True), vale3.Low, 0)
vale3["buy_start"] = np.where((vale3.Low < vale3.shift(1).mark_max) & (vale3.High > vale3.shift(1).mark_max), vale3.shift(1).mark_max, np.NaN)
vale3["sell_start"] = np.where((vale3.Low < vale3.shift(1).mark_min) & (vale3.High > vale3.shift(1).mark_min), vale3.shift(1).mark_min, np.NaN)
vale3["buy_stop"] = np.where((vale3.Low < vale3.shift(1).mark_max) & (vale3.High > vale3.shift(1).mark_max), vale3.shift(1).Low, np.NaN)
vale3["sell_stop"] = np.where((vale3.Low < vale3.shift(1).mark_min) & (vale3.High > vale3.shift(1).mark_min), vale3.shift(1).High, np.NaN)
print("vale3 - buy_start & buy_stop")
print(vale3[["buy_start", "buy_stop"]][(vale3.buy_start > 0)])
print()
print("vale3 - sell_start & sell_stop")
print(vale3[["sell_start", "sell_stop"]][(vale3.sell_start > 0)])
