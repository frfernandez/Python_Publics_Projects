from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np


def market_price(ticker, date_start, date_end):
    stock = []
    try:
        stock = yf.download(ticker + ".SA", start=date_start, end=date_end)
        if len(stock) == 0:
            stock = None
    except Exception as err:
        print("Sem registro de negociação para o ativo", ticker, "!")
        print("Mensagem original:", err)

    return stock


tick = "VALE3"
dict = {}
print()
try:
    dict = market_price(tick, datetime(2016, 10, 1), datetime(2019, 1, 1))

    if dict is not None:
        df = pd.DataFrame.from_dict(dict)

        print()
        print("Import ended !")

        print()
        print("Describe...")
        print(df.describe())

        print()
        print("All lines...")
        print(df)

        print()
        print("Ten first...")
        print(df.head(10))

        print()
        print("Ten last...")
        print(df.tail(10))

        print()
        print("Index...")
        print(df.index)

        print()
        print("Columns...")
        print(df.columns)

        print()
        pct_c = (df["Close"] / df["Open"]).apply(lambda x: x - 1) * 100
        print("Ten first percents...")
        print(pct_c.head(10))

        print()
        daily_log_returns = np.log(df["Close"].pct_change() + 1)
        print("Daily log returns...")
        print(daily_log_returns)
except Exception as err:
    print()
    print("Original message:", err)
