from binance import Client
import pandas
from datetime import datetime as dt
from assets_reader import assets_reader
from writeData import writeData
from Backtester import Backtester
from strategy import Strat


client = Client(None,None)

assets = assets_reader.reader()

df = {}; df2 = {}; df3 = {}; df4 = {};

csvFolder = r"C:/THE PATH OF THE CSV FILES/"
writer = writeData(client);

for asset in assets:
 
 name = f"\{asset}2023-15mFutures.csv"        #!!! 2023 IS BETWEEN 1 JAN 2023 - 1 FEB 2024
 name2 = f"\{asset}2023-1hFutures.csv"        #!!! 2022 IS BETWEEN 1 JAN 2022 - 1 FEB 2023
 name3 = f"\{asset}2023-4hFutures.csv"         #!!! 2023/123 5 MIN CHART NOT 15!!! FIRST 3 MONTHS OF 2023, 01-01-2023 - 01-04-2023
 name4 = f"\{asset}2023-1dFutures.csv"

 #writer.writeData(name , writer.getFuturesData(asset, client.KLINE_INTERVAL_5MINUTE, "1 January 2023" , "1 April 2023"))
 #writer.writeData(name2 , writer.getFuturesData(asset, client.KLINE_INTERVAL_1HOUR, "1 January 2022" , "1 February 2023"))
 #writer.writeData(name3 , writer.getFuturesData(asset, client.KLINE_INTERVAL_4HOUR, "1 January 2022" , "1 February 2023"))
 #writer.writeData(name4 , writer.getFuturesData(asset, client.KLINE_INTERVAL_1DAY, "1 January 2022" , "1 February 2023"))

 #Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
 titles = ['Open Time', 'Open Price', 'Highest Price', 'Lowest Price','Close Price' , 'Volume', 'Close Time', 'qat', 'nuot', 'tbbav', 'tbqav', 'ignore' ]

 #CREATES AN FRAME AND COPIES ELEMENTS WHICH ON CSV FILE.
 df[asset] = pandas.read_csv(csvFolder+name, names=titles)
 df2[asset] = pandas.read_csv(csvFolder+name2, names=titles )
 df3[asset] = pandas.read_csv(csvFolder+name3, names=titles )
 df4[asset] = pandas.read_csv(csvFolder+name4, names=titles )


 
print("START");
 
Strategy = Strat(df , df2 , df3 , df4 , assetList=assets)

Backtester = Backtester(df , Strategy, assets )

Backtester.Backtester()



