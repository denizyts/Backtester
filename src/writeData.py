from binance import Client
import csv 
import pandas

class writeData:
 
 def __init__(self, client):
  self.client = client;  
  self.folder = r"C:/THE PATH OF THE CSV FILES/"


 def getFuturesData(self , symbol, interval, start_time, end_time):
   klines = self.client.futures_historical_klines(symbol=symbol, interval=interval, start_str=start_time, end_str = end_time)
   return klines


#TAKES CANDLE DATA WITH CLIENT
 def getSpotData(self , coin,period,startdate,enddate):
  candles = self.client.get_historical_klines(coin, period, startdate, enddate)
  return candles

#WRITES DATAS INTO A CSV FILE
 def writeData(self , name , candles):

  extension = name 
  csvFile = open(self.folder+extension ,'w',newline = '')
  printer = csv.writer(csvFile,delimiter = ',')
    
    #WITH THIS FOR LOOP EACH ELEMENT OF CANDLE LIST WRITTEN ON ONLY ONE LINE SO ON CSV FILE THERE ARE NO LIST, LINES EXIST ONLY !
  for candle in candles:
   printer.writerow(candle)    
  csvFile.close()


  