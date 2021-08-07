from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
        daily_log_returns = np.log(df["Close"].pct_change() + 1)
        print("Daily log returns...")
        print(daily_log_returns)

        plt.hist(daily_log_returns, bins=100)
        plt.show()
except Exception as err:
    print()
    print("Original message:", err)
