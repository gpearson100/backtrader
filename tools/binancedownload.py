from binance.client import Client
import pandas as pd
import numpy as np

"""
# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# fetch 30 minute klines for the last month of 2017
klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

https://python-binance.readthedocs.io/en/latest/market_data.html#id7
"""

client = Client('', '')
def getCandles(_symbol="",_interval="",_startTime="",_endTime=""):
    df = pd.DataFrame(columns= ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time'])
    #candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, startTime="a", endTime="b")
    candles = client.get_klines(symbol=_symbol, interval=_interval, startTime=_startTime, endTime=_endTime)

    opentime, lopen, lhigh, llow, lclose, lvol, closetime = [], [], [], [], [], [], []

    for candle in candles:
        opentime.append(candle[0])
        lopen.append(candle[1])
        lhigh.append(candle[2])
        llow.append(candle[3])
        lclose.append(candle[4])
        lvol.append(candle[5])
        closetime.append(candle[6])

    df['Open_time'] = opentime
    df['Open'] = np.array(lopen).astype(np.float)
    df['High'] = np.array(lhigh).astype(np.float)
    df['Low'] = np.array(llow).astype(np.float)
    df['Close'] = np.array(lclose).astype(np.float)
    df['Volume'] = np.array(lvol).astype(np.float)
    df['Close_time'] = closetime
    return df