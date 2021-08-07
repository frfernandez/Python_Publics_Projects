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
start_date = datetime(year=2016, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)

data = get(tickers, start_date, end_date)
data = data.reset_index()
data = data.set_index(["date", "ticker"]).sort_index()

close = data.reset_index().pivot(index="date", columns="ticker", values="Close")
log_returns = np.log(close.dropna()).diff()
print("log_returns")
print(log_returns.head())

axis=[]
for d in log_returns:
    axi = go.Scatter(x=log_returns.index,
                     y=log_returns[d].cumsum(),
                     name=d,
                     opacity=1)

    axis.append(axi)

simple_plot(axis, title="Cumulative log returns")

axis=[]
for d in log_returns:
    axi = go.Scatter(x=log_returns.index,
                     y=100 * (np.exp(log_returns[d].cumsum()) - 1),
                     name=d,
                     opacity=1)

    axis.append(axi)

simple_plot(axis, title="Total relative returns (%)")
