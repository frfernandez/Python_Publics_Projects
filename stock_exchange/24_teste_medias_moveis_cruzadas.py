from datetime import datetime
from enum import Enum

import pandas as pd
import pandas_datareader.data as pdr


class Operacao(Enum):
    INICIO = 1
    COMPRAR = 2
    COMPRANDO = 3
    COMPRADO = 4
    VENDER = 5
    VENDENDO = 6
    VENDIDO = 7


def get(tickers, start_date, end_date):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    datas = map(data, tickers)
    return pd.concat(datas, keys=tickers, names=["ticker", "date"])


tickers = ["AAPL", "MSFT", "^GSPC"]
start_date = datetime(year=2018, month=3, day=1,
                      hour=0, minute=0, second=0, microsecond=0)
end_date = datetime(year=2018, month=7, day=1,
                    hour=23, minute=59, second=59, microsecond=999999)

data = get(tickers, start_date, end_date)

msft = data.loc["MSFT"].dropna()
msft = msft["2018-01-01":]
short_rolling_msft = msft.Close.rolling(window=9).mean().dropna()
long_rolling_msft = msft.Close.rolling(window=21).mean().dropna()

print("short_rolling_msft")
print(short_rolling_msft)
print()
print("short_rolling_msft.tail(1)")
print(short_rolling_msft.tail(1))
print()
print("long_rolling_msft")
print(long_rolling_msft)
print()
print("long_rolling_msft.tail(1)")
print(long_rolling_msft.tail(1))

short_rolling = short_rolling_msft.to_frame()
long_rolling = long_rolling_msft.to_frame()

print()
print("short_rolling")
print(short_rolling)
print()
print("long_rolling")
print(long_rolling)

posicao = Operacao(1)

"""
Se a média curta estiver MENOR que a média longa deve ser realizada a COMPRA quando elas se cruzarem.
Se a média curta estiver MAIOR que a média longa deve ser realizada a VENDA quando elas se cruzarem.
Quando o programa assumir o estado COMPRANDO ou VENDENDO este fará uma analise de pagamento de taxas 
antes de realizar a operação.
Quando o programa assumir o estado VENDER este fará uma analise de prejuízo antes de realizar a operação.
"""

print()
print("short_rolling - loop for")
for data_hora, media_curta in short_rolling.iterrows():
    print(data_hora, "|", str(data_hora).replace("00:00:00", "23:59:59"), "|", media_curta.Close)
    media_longa = long_rolling[data_hora:str(data_hora).replace("00:00:00", "23:59:59")].Close

    print()
    print("media_longa")
    print(media_longa)
    print()

    if not media_longa.empty:
        print("media_longa: ", media_longa[0])

        if posicao == Operacao.INICIO:
            if media_curta.Close <= media_longa[0]:
                posicao = Operacao(2)
                print(posicao.name)
            else:
                posicao = Operacao(5)
                print(posicao.name)

        if posicao == Operacao.COMPRAR:
            if media_curta.Close > media_longa[0]:
                posicao = Operacao(3)
                print(posicao.name)
                posicao = Operacao(4) # Apenas para testes.
                print(posicao.name)
        elif posicao == Operacao.COMPRADO:
            if media_curta.Close < media_longa[0]:
                posicao = Operacao(6)
                print(posicao.name)
                posicao = Operacao(7) # Apenas para testes.
                print(posicao.name)
