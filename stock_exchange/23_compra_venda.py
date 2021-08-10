from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr


def get(tickers, start_date, end_date):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    datas = map(data, tickers)
    return pd.concat(datas, keys=tickers, names=["ticker", "date"])


class TradeType(Enum):
    NONE = 0
    LONG = 1
    SHORT = -1


class BackTest:
    def __init__(self, stock, signals, **kwargs):
        self._position = 0
        self._position_opened = False
        self._amount = 0
        self._stock = stock
        self.trades = []
        self._signals = signals
        self._status = None
        self._std_qty_shares = 100
        self._reverse = True

        self._show_logs = ("log" in kwargs) and (kwargs["log"])

        self.win_trades = 0
        self.loss_trades = 0

    def _get_win_trades(self, x):
        return x >= 0

    def _get_loss_trades(self, x):
        return x < 0

    def _trade(self, position, index):
        """
        :position:LONG or SHORT
        :index: index of stock list
        """
        # if has a opened trading, then it will close the position
        if self._position_opened:
            # set the operating profit
            profit = ((self._std_qty_shares * self._stock.Close[index]) - self._amount) * (self._position * - 1)

            # add profit to trade list
            self.trades.append(profit)

            # close the position
            self._position_opened = False

            # log
            if self._show_logs:
                print(f"Opened[[self._amount]] -> Closed[{self._std_qty_shares * self._stock.Close[index]}] {position.name}")
        else:
            # if it hans't an opnend position, open it.
            self._position_opened = True
            self._amount = self._std_qty_shares * self._stock.Close[index]

    def start(self):
        """
        execute the backtest
        """
        for index, item in self._stock.iterrows():
            # for long signal (buy)
            if TradeType(self._signals.signal[index]) == TradeType.LONG:
                # Last signal was long signal ?
                # Go to next iteration
                if TradeType(self._position) == TradeType.LONG:
                    continue

                self._position = self._signals.signal[index]
                # if has a opened short position, then sell
                if self._position_opened:
                    self._trade(TradeType.SHORT, index)
                    # because i'm want to revert my position
                    if self._reverse:
                        self._trade(TradeType.SHORT, index)
                    else:
                        # Ok, I need to open a position
                        self._trade(TradeType.LONG, index)

                # for short signal (sell)
                if TradeType(self._signals.signal[index]) == TradeType.SHORT:
                    if TradeType(self._position) == TradeType.SHORT:
                        continue

                    self._position = self._signals.signal[index]

                    if self._position_opened:
                        self._trade(TradeType.LONG, index)
                        if self._reverse:
                            self._trade(TradeType.SHORT, index)
                    else:
                        self._trade(TradeType.SHORT, index)

        self.win_trades = len(list(filter(self._get_win_trades, self.trades)))
        self.loss_trades = len(list(filter(self._get_loss_trades, self.trades)))


def build_hilo_signal_list(window=5):
    aapl_high_avg = aapl.High.rolling(window=window).mean()
    aapl_low_avg = aapl.Low.rolling(window=window).mean()
    aapl_hilo = pd.DataFrame(index=aapl.index)
    aapl_hilo["high"] = np.where(aapl.Close > aapl_high_avg, 1, 0)
    aapl_hilo["low"] = np.where(aapl.Close < aapl_low_avg, 1, 0)
    aapl_hilo["signal"] = (aapl_hilo.high - aapl_hilo.low)

    return aapl_hilo


def build_cross_avg_signal_list(short_window=5, long_window=9):
    aapl_short_avg = aapl.Close.rolling(window=short_window).mean()
    aapl_long_avg = aapl.Close.rolling(window=long_window).mean()
    aapl_cross_avg = pd.DataFrame(index=aapl.index)
    aapl_cross_avg["signal"] = np.where(aapl_short_avg > aapl_long_avg, 1, -1)

    return aapl_cross_avg


tickers = ["AAPL", "MSFT", "^GSPC"]
start_date = datetime(year=2018, month=1, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=12, day=31,
                    hour=0, minute=0, second=0, microsecond=0)

data = get(tickers, start_date, end_date)
aapl = data.loc["AAPL"].dropna()

best_profit = None
print(f"BackTest HiLo - Start Date: {start_date} / End Date: {end_date}")
print("-" * 100)

for window in range(2, 22):
    signals = build_hilo_signal_list(window=window)
    bt = BackTest(aapl, signals, log=False)
    bt.start()

    profit = sum(bt.trades)
    if (best_profit is None) or (best_profit[1] < profit):
        best_profit = (window, profit)

    print(f"Profit for window = {window}:{profit}")

print("-" * 100)
print(f"Best Profit: Window = {best_profit[0]}:{best_profit[1]}")
print()

best_profit = None
print(f"BackTest Cross Avg - Start Date: {start_date} / End Date: {end_date}")
print("-" * 100)

for short_window in range(2, 22):
    for long_window in range(2, 22):
        signals = build_cross_avg_signal_list(short_window=short_window, long_window=long_window)
        bt = BackTest(aapl, signals, log=False)
        bt.start()

        profit = sum(bt.trades)
        if (best_profit is None) or (best_profit[1] < profit):
            best_profit = ((short_window, long_window), profit)

        print(f"Profit for window = {short_window}/{long_window}:{profit}")

print("-" * 100)
print(f"Best Profit: Window = {best_profit[0]}:{best_profit[1]}")
