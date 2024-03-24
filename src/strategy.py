
import pandas_ta 
from datetime import datetime
import vwapCalc
import vwapCalcV2


class Strat:      

 def __init__(self , df1 , df2 , df3 , df4 , assetList):
  
  self.df1 = df1; self.df2 = df2; self.df3 = df3; self.df4 = df4;
  

  self.btc_string = "BTCUSDT"

  self.zscore1 = {}; self.zscore2 = {}; self.zscore3 = {}; self.zscore4 = {};
  
  
  self.vwap_df1 = {}; self.vwap_df2 = {}; self.vwap_df3 = {}; self.vwap_df4 = {};

  self.rsi1 = {};

  self.index_constant1 = 0; self.index_constant2 = 0; self.index_constant3 = 0; 

  self.superTrend = {};
  


  for asset in assetList:
   

   self.zscore1[asset] = pandas_ta.zscore(df1[asset]["Close Price"] , length=10);
   self.zscore2[asset] = pandas_ta.zscore(df2[asset]["Close Price"] , length=90);
   self.zscore3[asset] = pandas_ta.zscore(df3[asset]["Close Price"] , length=100);
   self.zscore4[asset] = pandas_ta.zscore(df4[asset]["Close Price"] , length=10);

   self.rsi1[asset] = pandas_ta.rsi(df1[asset]["Close Price"] , length=8);
   
   self.vwap_df1[asset] = vwapCalcV2.Calculate(df1[asset]["Highest Price"] , df1[asset]["Lowest Price"] , 
                                                      df1[asset]["Close Price"] , df1[asset]["Volume"] , anchor = 10 , stdev_multp = 0.1);
  
   self.vwap_df2[asset] = vwapCalcV2.Calculate(df2[asset]["Highest Price"] , df2[asset]["Lowest Price"] , 
                                                      df2[asset]["Close Price"] , df2[asset]["Volume"] , anchor = 8 , stdev_multp=0.1);
  
   self.vwap_df3[asset] = vwapCalcV2.Calculate(df3[asset]["Highest Price"] , df3[asset]["Lowest Price"] ,     
                                                      df3[asset]["Close Price"] , df3[asset]["Volume"] , anchor = 8 , stdev_multp=0.1);
  
   self.vwap_df4[asset] = vwapCalcV2.Calculate(df4[asset]["Highest Price"] , df4[asset]["Lowest Price"] ,
                                                      df4[asset]["Close Price"] , df4[asset]["Volume"] , anchor = 8 , stdev_multp=0.1);
  
   self.superTrend[asset] = pandas_ta.supertrend(df1[asset]["Highest Price"] , df1[asset]["Lowest Price"] , df1[asset]["Close Price"] , 10 , 10.0)['SUPERT_10_10.0']
   
   

  for i in range(len(df1[self.btc_string]["Close Price"])):
   if(df1[self.btc_string]["Close Price"][i] == df2[self.btc_string]["Close Price"][0]):
    self.index_constant1 = i+1; 
    print("Second period index constant is " , self.index_constant1); break;
 
  for i in range(len(df1[self.btc_string]["Close Price"])):
   if(df1[self.btc_string]["Close Price"][i] == df3[self.btc_string]["Close Price"][0]):
    self.index_constant2 = i+1; 
    print("Third period index constant is " , self.index_constant2); break;

  for i in range(len(df1[self.btc_string]["Close Price"])):
   if(df1[self.btc_string]["Close Price"][i] == df4[self.btc_string]["Close Price"][0]):
    self.index_constant3 = i+1; 
    print("Fourth period index constant is " , self.index_constant3); break;
  

##############################################################
 def BuyConditionCheck(self, index , asset):
  
  if(index > self.index_constant3*10):
   
   cons1 = int(index / self.index_constant1);
   cons2 = int(index / self.index_constant2);
   cons3 = int(index / self.index_constant3);

  
   condition1 = self.zscore1[asset][index] < -1.5;       #15m
   rsiCondition = self.rsi1[asset][index] < 30;
   reversalCondition = self.zscore1[asset][index-1] < self.zscore1[asset][index];
   volumeCondition = self.df1[asset]["Volume"][index] > self.df1[asset]["Volume"][index-1];

   trend = self.superTrend[asset][index] < self.df1[asset]["Close Price"][index];






   if(condition1 and rsiCondition and reversalCondition and volumeCondition and trend):
    return True
   else:
    return False
   
 def SellConditionCheck(self, index , asset):
  
  if(index > self.index_constant3*10):
   
   cons1 = int(index / self.index_constant1);
   cons2 = int(index / self.index_constant2);
   cons3 = int(index / self.index_constant3);

   condition1 = self.zscore1[asset][index] > 1.8;       #15m
   rsiCondition = self.rsi1[asset][index] > 70;
   reversalCondition = self.zscore1[asset][index-1] > self.zscore1[asset][index];
   volumeCondition = self.df1[asset]["Volume"][index] > self.df1[asset]["Volume"][index-1];


   trend = self.superTrend[asset][index] > self.df1[asset]["Close Price"][index];


   if(condition1 and rsiCondition and reversalCondition and volumeCondition and trend):
    return True
   else:
    return False
   

 
 def long_close(self , index , asset):
  
  if(index < self.index_constant3*8):return False;
  
  cons1 = int(index / self.index_constant1);
  cons2 = int(index / self.index_constant2);
  cons3 = int(index / self.index_constant3);

  condition1 = self.zscore1[asset][index] > 1.5;       #15m
  rsiCondition = self.rsi1[asset][index] > 65;
  reversalCondition = self.zscore1[asset][index-1] > self.zscore1[asset][index];
  oppositeTrend = self.superTrend[asset][index] > self.df1[asset]["Close Price"][index];

  close_conds = (condition1 and rsiCondition and reversalCondition) or oppositeTrend; 

  

  if(close_conds):return True;
  else:return False;
  
    
 def short_close(self , index , asset):
  
  if(index < self.index_constant3*8):return False;
  
  cons1 = int(index / self.index_constant1);
  cons2 = int(index / self.index_constant2);
  cons3 = int(index / self.index_constant3);

  condition1 = self.zscore1[asset][index] < -1.8;       #15m
  rsiCondition = self.rsi1[asset][index] < 35;
  reversalCondition = self.zscore1[asset][index-1] < self.zscore1[asset][index];

  oppositeTrend = self.superTrend[asset][index] < self.df1[asset]["Close Price"][index];

  
  close_conds = (condition1 and rsiCondition and reversalCondition) or oppositeTrend; 

  if(close_conds):return True;
  else:return False;
   

