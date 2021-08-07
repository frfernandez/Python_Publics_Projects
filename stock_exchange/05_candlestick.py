from datetime import datetime
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
start_date = datetime(year=2018, month=11, day=11,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=11, day=18,
                    hour=0, minute=0, second=0, microsecond=0)
data = get(tickers, start_date, end_date)
trace = go.Candlestick(x=data.loc["MSFT"].index,
                       open=data.loc["MSFT"].Open,
                       high=data.loc["MSFT"].High,
                       low=data.loc["MSFT"].Low,
                       close=data.loc["MSFT"].Close)
data = [trace]

print("data")
print(data)

simple_plot(data, title="Candlestick plot")
