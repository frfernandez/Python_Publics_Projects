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
start_date = datetime(year=2018, month=6, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2019, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)
window = 21

data = get(tickers, start_date, end_date)

msft = data.loc["MSFT"].dropna()
msft = msft["2018-06-01":]
MA = msft.Close.rolling(window=window).mean()

trace_avg = go.Scatter(x=MA.index,
                       y=MA,
                       name="MSFT MA(21)",
                       line=dict(color="#72ac00"),
                       opacity=1)

trace_candles = go.Candlestick(x=msft.index,
                               open=msft.Open,
                               high=msft.High,
                               low=msft.Low,
                               close=msft.Close,
                               name="Price")

data = [trace_avg, trace_candles]
simple_plot(data, "Simple moving average")
