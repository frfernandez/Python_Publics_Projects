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
r_t = log_returns.tail(1).transpose()
weights_vector = pd.DataFrame(1 / 3, index=r_t.index, columns=r_t.columns)
print("weights_vector")
print(weights_vector)

portfolio_log_return = weights_vector.transpose().dot(r_t)
print()
print("portfolio_log_return")
print(portfolio_log_return)

weights_matrix = pd.DataFrame(1 / 3, index=log_returns.index, columns=log_returns.columns)
print()
print("weights_matrix.head()")
print(weights_matrix.head())

temp_var = weights_matrix.dot(log_returns.transpose())
print()
print("temp_var.tail()")
print(temp_var.tail())

portfolio_log_returns = pd.Series(np.diag(temp_var), index=log_returns.index)
portfolio_log_returns = portfolio_log_returns[1:]
print()
print("portfolio_log_returns.tail()")
print(portfolio_log_returns.tail())

axis = go.Scatter(x=portfolio_log_returns.index,
                  y=portfolio_log_returns.cumsum(),
                  opacity=1)

simple_plot(axis, title="Portfolio cumulative log returns")

total_relative_returns = (np.exp(portfolio_log_returns.cumsum()) - 1)

axis = go.Scatter(x=total_relative_returns.index,
                  y=total_relative_returns * 100,
                  opacity=1)

simple_plot(axis, title="Portfolio total relative returns (%)")
