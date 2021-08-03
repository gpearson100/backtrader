import backtrader as bt
import pandas as pd
import datetime as dt

fileData = "C:\\Dev\\backtrader\\datas\\Binance_BNBUSDT_1m_20210704-20210803_index.csv"



class PrintClose(bt.Strategy):

    def __init__(self):
        #Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') #Print date and close

    def next(self):
        self.log('Close: ', self.dataclose[0])

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Add data feed to Cerebro
#df = pd.read_pickle(fileData,'infer')
df = pd.read_csv(fileData,parse_dates=True)

#df['Open_time'] = pd.to_datetime(df['Open_time']).dt.to_pydatetime()
data = bt.feeds.PandasDirectData(dataname=df)

cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(PrintClose)

#Run Cerebro Engine
cerebro.run()