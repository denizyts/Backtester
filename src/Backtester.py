from datetime import datetime as dt
import wallet_value_graph

class Backtester:
 
 def __init__(self, df , strategy , assets):
 
  
  self.df = df
  self.strategy = strategy
  self.assets = assets
 
 def Backtester(self, InitialBalance , BuyUnit_initial , leverage):

  self.TakerFee = 0.05  #BECAUSE %0.05
  self.MakerFee = 0.02 #BECAUSE %0.02
  self.initial_balance = InitialBalance
  self.Balance = self.initial_balance
  self.BuyUnit_initial = BuyUnit_initial;
  self.BuyUnit = self.BuyUnit_initial
  self.leverage = leverage
  self.TP_percentage = 5
  self.SL_percentage = 0.910
  self.SHORT_TP = 0.2
  self.SHORT_SL = 1.090
  self.assetSize = {}
  self.AveragePrice = {}
  self.long_sl_counter = {}
  self.long_tp_counter = {}
  self.short_tp_counter = {}
  self.short_sl_counter = {}
  self.short_close_counter = {}
  self.long_close_counter = {}  
  self.earn_list = {}
  self.position_name = {}
  self.new_position = {} 
  self.wallet_value_list = []
  self.total_earning = 0
  self.asset_in_position_counter = 0
  self.greatest_decrease_of_balance = 0
  self.prev_balance = self.Balance
  self.prev_balance_withoutOperations = self.Balance
  self.decreaseList = []
  self.totalFee = 0
  self.islemSayisi = 0
  self.greatest_decrease_of_balance_time = 0
  self.long_close_earn = {}
  self.short_close_earn = {}
  
 
  for asset in self.assets:
   self.assetSize[asset] = 0
   self.long_tp_counter[asset] = 0
   self.long_sl_counter[asset] = 0
   self.short_tp_counter[asset] = 0
   self.short_sl_counter[asset] = 0
   self.long_close_counter[asset] = 0
   self.short_close_counter[asset] = 0
   self.earn_list[asset] = 0
   self.position_name[asset] = "empty"    #no means no position , also there are long and short and empty for inialize
   self.new_position[asset] = False
   self.long_close_earn[asset] = 0;
   self.short_close_earn[asset] = 0;

  for i in range(len(self.df["BTCUSDT"]["Close Price"])):
   
   if(self.Balance > 100):
    self.BuyUnit = self.BuyUnit_initial
    #self.BuyUnit = self.Balance / 40;
   else:
    self.BuyUnit = self.BuyUnit_initial 
 

   for asset in self.assets:

    self.new_position[asset] = False   #avoids if position attempts to get closed in same candle, occurs in greater time frames. like 1 hour
    
    if(self.strategy.BuyConditionCheck(index=i , asset=asset) == True and (self.position_name[asset] == "no" or self.position_name[asset] == "empty") and self.Balance > self.BuyUnit ):
     self.long_enter(index=i , asset=asset)
     self.new_position[asset] = True
     self.asset_in_position_counter = self.asset_in_position_counter + 1
   
    if(self.position_name[asset] == "long" and self.df[asset]["Highest Price"][i] > self.AveragePrice[asset]*self.TP_percentage and self.new_position[asset] == False):
     self.take_profit(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1
   
    if(self.position_name[asset] == "long"  and self.df[asset]["Lowest Price"][i] < self.AveragePrice[asset]*self.SL_percentage and self.new_position[asset] == False):
     self.stop_loss(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1

    if(self.position_name[asset] == "long" and self.strategy.long_close(index=i , asset=asset) == True and self.new_position[asset] == False): 
     self.close_long(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1

    if(self.strategy.SellConditionCheck(index=i , asset=asset) == True and (self.position_name[asset] == "no" or self.position_name[asset] == "empty") and self.Balance > self.BuyUnit ):
     self.short_enter(index=i , asset=asset)
     self.new_position[asset] = True
     self.asset_in_position_counter = self.asset_in_position_counter + 1

    if(self.position_name[asset] == "short" and self.df[asset]["Highest Price"][i] > self.AveragePrice[asset]*self.SHORT_SL and self.new_position[asset] == False):
     self.short_stop_loss(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1

    if(self.position_name[asset] == "short" and self.df[asset]["Lowest Price"][i] < self.AveragePrice[asset]*self.SHORT_TP and self.new_position[asset] == False):
     self.short_take_profit(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1

    if(self.position_name[asset] == "short" and self.strategy.short_close(index=i , asset=asset) == True and self.new_position[asset] == False): 
     self.close_short(index=i , asset=asset)
     self.asset_in_position_counter = self.asset_in_position_counter - 1

     
   if(i%96 == 0):
    wallet_value = self.Balance + (self.asset_in_position_counter * self.BuyUnit)
    self.wallet_value_list.append(wallet_value)
    if( self.greatest_decrease_of_balance < self.prev_balance - wallet_value): 
     self.greatest_decrease_of_balance = self.prev_balance - wallet_value;
     self.greatest_decrease_of_balance_time = dt.fromtimestamp(self.df["BTCUSDT"]["Close Time"][i]/1000);
    if(self.prev_balance > wallet_value): self.decreaseList.append(self.prev_balance - wallet_value)
    self.prev_balance = wallet_value
    self.prev_balance_withoutOperations = self.Balance;
    

  for asset in self.assets:
   print(asset)
   print("LONG -> Tp counter , Sl counter , Close Counter:  " , self.long_tp_counter[asset] , " " , self.long_sl_counter[asset] , " " , self.long_close_counter[asset] )
   print("SHORT -> Tp counter , Sl counter , Close Counter: " , self.short_tp_counter[asset] , " " , self.short_sl_counter[asset] , " " , self.short_close_counter[asset])  
   print("Total earn from " , asset , " :" , self.earn_list[asset])
   print("Long Close Earn " , self.long_close_earn[asset])
   print("Short Close Earn " , self.short_close_earn[asset])
   self.total_earning = self.total_earning + self.earn_list[asset]
   if(self.position_name[asset] == "long" or self.position_name[asset] == "short"):
    print("Still in operation !!!")
   print("---------------------------------------------")
  print("Total Earning: " , self.total_earning)
  print("Greatest Decrease of balance " , self.greatest_decrease_of_balance)
  print("Greatest Decrease of balance time " , self.greatest_decrease_of_balance_time)
  print("Total Fee " , self.totalFee)
  print("Total islem sayisi " , self.islemSayisi)
  print("Last Balance " , self.Balance)
  self.decreaseList.sort()
  print(self.decreaseList)
  wallet_value_graph.draw(self.wallet_value_list )




 def long_enter(self,  index ,asset):
  self.assetSize[asset] = (self.BuyUnit*self.leverage) / self.df[asset]["Close Price"][index] 
  self.AveragePrice[asset] = self.df[asset]["Close Price"][index]
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.TakerFee )
  self.Balance = self.Balance - (self.df[asset]["Close Price"][index]*(self.assetSize[asset]/self.leverage)) - fee
  self.position_name[asset] = "long"
  self.totalFee += fee
  self.islemSayisi += 1

  self.printer(index , asset , difference=0 , operationName="Long Enter")
  


 def stop_loss(self, index , asset):
  Loss = self.assetSize[asset] * (self.AveragePrice[asset]*self.SL_percentage - self.AveragePrice[asset]) #negative float.
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.Balance = self.Balance + Loss + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee   
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + Loss - (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.long_sl_counter[asset] = self.long_sl_counter[asset] + 1
  self.position_name[asset] = "no" 
  self.totalFee += fee

  self.printer(index , asset , difference=Loss , operationName="Long Stop Loss")
 


 def take_profit(self, index , asset):
  Profit = self.assetSize[asset] * (self.AveragePrice[asset]*self.TP_percentage - self.AveragePrice[asset])
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.Balance = self.Balance + Profit + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + Profit - (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.long_tp_counter[asset] = self.long_tp_counter[asset] + 1
  self.position_name[asset] = "no" 
  self.totalFee += fee

  self.printer(index , asset , difference=Profit , operationName="Long Take Profit")
  

 def short_enter(self,  index ,asset):
  self.assetSize[asset] = (self.BuyUnit*self.leverage) / self.df[asset]["Close Price"][index] 
  self.AveragePrice[asset] = self.df[asset]["Close Price"][index]
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.TakerFee )
  self.Balance = self.Balance - (self.df[asset]["Close Price"][index]*(self.assetSize[asset]/self.leverage)) - fee
  self.position_name[asset] = "short" 
  self.totalFee += fee
  self.islemSayisi += 1

  self.printer(index , asset , difference=0 , operationName="Short Enter")
  

 def short_take_profit(self, index , asset):
  Profit = self.assetSize[asset] * (self.AveragePrice[asset] - self.AveragePrice[asset]*self.SHORT_TP)
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.Balance = self.Balance + Profit + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + Profit
  self.short_tp_counter[asset] = self.short_tp_counter[asset] + 1
  self.position_name[asset] = "no"
  self.totalFee += fee

  self.printer(index , asset , difference=Profit , operationName="Short Take Profit")
  

 def short_stop_loss(self, index , asset):
  Loss = self.assetSize[asset] * (self.AveragePrice[asset] - self.AveragePrice[asset]*self.SHORT_SL) #negative float.
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.MakerFee )
  self.Balance = self.Balance + Loss + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee   
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + Loss
  self.short_sl_counter[asset] = self.short_sl_counter[asset] + 1
  self.position_name[asset] = "no" 
  self.totalFee += fee

  self.printer(index , asset , difference=Loss , operationName="Short Stop Loss")
  

 def close_short(self, index, asset):
  difference = self.assetSize[asset] * (self.AveragePrice[asset] - self.df[asset]["Close Price"][index]) #negative or positive ffloat depends on closeprices
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.TakerFee )
  self.Balance = self.Balance + difference + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee 
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + difference - fee
  self.short_close_counter[asset] = self.short_close_counter[asset] + 1 
  self.position_name[asset] = "no" 
  self.short_close_earn[asset] += difference;
  self.totalFee += fee
 
  self.printer(index , asset , difference=difference , operationName="Short Close")
  
 def close_long(self , index, asset):
  difference = self.assetSize[asset] * (self.df[asset]["Close Price"][index] - self.AveragePrice[asset]) #negative or pesitive depends on closeprice.
  fee = (((self.assetSize[asset]*self.df[asset]["Close Price"][index]) / 100) * self.TakerFee )
  self.Balance = self.Balance + difference + (self.AveragePrice[asset]*(self.assetSize[asset]/self.leverage)) - fee   
  self.assetSize[asset] = 0
  self.AveragePrice[asset] = 0
  self.earn_list[asset] = self.earn_list[asset] + difference - fee
  self.long_close_counter[asset] = self.long_close_counter[asset] + 1
  self.position_name[asset] = "no" 
  self.long_close_earn[asset] += difference;
  self.totalFee += fee
 
  self.printer(index , asset , difference=difference , operationName="Long Close")
  


 def printer(self , index , asset , difference , operationName):
  
  print(operationName , " " ,  asset);
  print("Time " , dt.fromtimestamp((self.df[asset]["Close Time"][index]) / 1000))
  print("Price : " , self.df[asset]["Close Price"][index])
  print("Difference : " , difference)
  print("asset size becomes " , self.assetSize[asset])
  print("Balance becomes " , self.Balance , " USD")
  print("------------------------------------------");