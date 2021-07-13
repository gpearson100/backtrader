from binance.client import Client
from binance.enums import HistoricalKlinesType
import pandas as pd
import numpy as np
import re, datetime
from api import api_key, api_secret, proxies

"""
# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# fetch 30 minute klines for the last month of 2017
klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

https://python-binance.readthedocs.io/en/latest/market_data.html#id7

List[Dict[str, str]]
print(testy(d,"BNB"))
x = [d[key] for key in d.keys() if re.match(key, "BNB")]

  get_historical_klines_generator(symbol, interval, start_str, end_str=None, 
    klines_type: binance.enums.HistoricalKlinesType = <HistoricalKlinesType.SPOT: 1>)
"""
client = Client(api_key, api_secret, {'proxies': proxies})

_symbol = "BNBUSDT"
_interval = Client.KLINE_INTERVAL_15MINUTE
_startTime = int((datetime.datetime.now() - datetime.timedelta(30)).timestamp() * 1000)
_endTime = int(datetime.datetime.now().timestamp() * 1000)
getSymbols = False

try:
    if getSymbols:
        allSymbols = client.get_all_tickers()
        f = open("symbols.txt", "w")
        for symbol in allSymbols:
            f.write(symbol["symbol"]+ "\n")
        f.flush()
        f.close()
except IOError as strerror :
    print ("I/O error: {1}".format( strerror))


def getCandles(_symbol=_symbol,_interval=_interval,_startTime=_startTime,_endTime=_endTime):

    df = pd.DataFrame(columns= ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    # df = pd.DataFrame(columns= ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time'])
    #candles = client.get_klines(symbol=_symbol, interval=_interval,startTime=str(_startTime), endTime=str(_endTime))
    candles = client.get_historical_klines_generator(symbol=_symbol, interval=_interval,start_str=_startTime, end_str=_endTime,klines_type=HistoricalKlinesType.SPOT)
    opentime, lopen, lhigh, llow, lclose, lvol = [], [], [], [], [], []
    #opentime, lopen, lhigh, llow, lclose, lvol, closetime = [], [], [], [], [], [], []

    for candle in candles:
        oTime = datetime.datetime.fromtimestamp(int(candle[0] / 1000)).strftime('%Y-%m-%d')
        opentime.append(oTime)
        lopen.append(candle[1])
        lhigh.append(candle[2])
        llow.append(candle[3])
        lclose.append(candle[4])
        lvol.append(candle[5])
     #   cTime = datetime.datetime.fromtimestamp(int(candle[6] / 1000)).strftime('%Y-%m-%d')
     #   closetime.append(cTime)

    
    df['Open_time'] = opentime
    df['Open'] = np.array(lopen).astype(float)
    df['High'] = np.array(lhigh).astype(float)
    df['Low'] = np.array(llow).astype(float)
    df['Close'] = np.array(lclose).astype(float)
    df['Volume'] = np.array(lvol).astype(float)
  #  df['Close_time'] = closetime
    return df

#ts = str(int(datetime.datetime.now().utcnow().timestamp()))

results = getCandles()
startTimestamp = datetime.datetime.fromtimestamp(int(_startTime / 1000)).strftime('%Y%m%d')
endTimeStamp = datetime.datetime.fromtimestamp(int(_endTime / 1000)).strftime('%Y%m%d')
fileName = "Binance_" + _symbol+"_" + _interval + "_" + startTimestamp + "-" + endTimeStamp
results.to_csv( 'datas/' + fileName + '.csv', index=False)
print("Done")