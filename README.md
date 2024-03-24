# Futures Backtester for financial markets.

This project allows you to test your strategies on historical price data.
Initially the csv files are Binance Futures historical data.


If you have any problem send mail to me by using the adress on my profile
*https://github.com/denizyts*

## Table of Contents

- [Why Should I Use This Backtester](#Why)
- [Details](#Details)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Why Should I Use This Backtester ?
-This Script allows to do testing on large csv files, it means you can do test on a asset from 1999 to 2024.
  
-High flexibility, by adding few lines of code you can make big changes.

-Multiple Intervals, you can do backtest at 15 min timeframe but same time you can check the data on 1 hour timeframe.

-Allows multiple assets, you can test your strategies with several assets.

## Details

### Historical Data
The csv files are fetched from the Binance Futures using the binance module. You can change the csv files with yours but be careful about lengths, the files with same interval and same period must have equal lengths.
Also you can fetch historical data from yahoofinance or anywhere you wish.
Please set the path of the csv files before run.

For more information binance api:
*https://binance-docs.github.io/apidocs/futures/en/*

### Binance Module
*https://pypi.org/project/binance.py/*
A python3 binance API wrapper.
Historical datas are fetched from api by using Binance Client. For fetching historical data no API required so you can create instance object client Client(None , None).

### Multiple Timeframes
At *main.py* initially there are 4 timeframes those are 15m , 1h , 4h , 1d. Those historical datas fetched already, Strategies are very flexible with this multiple timeframes.
Also you can add more timeframes, but backtest are done at smallest interval , it means the main loop has length of the smallest period csv.

### Assets
*assets.txt* files are store asset names of coins, at the design those are like *BTCUSDT* *SOLUSDT*. 
! Please delete empty lines on assets.txt files. !
If you are doing tests on stocks you must change asset names related with csv names.

### Indicators
At *strategy.py* indicators are from pandas_ta, easy and fast to use for more information:
*https://github.com/twopirllc/pandas-ta*

Also there are vwapCalcV2 which implemented by me. You can check it:
*https://github.com/denizyts/vwapCalc*

### Wallet Value Graph
Plots the change of balance by using matplotlib. 
With this it is more easy to see increases or decreases on the balance.

### Write Data into a CSV
On main set the names then call the *writer.WriterData()* there are command lines shows how to call it, Interval type is enum from binance module.

### TPSL & Exit
Backtester class includes many options for your strategy thoose are Take Profit , Stop Loss and Exits , Thoose methods can be combined or can be used indivudally, set TP and SL levels 
You can change the returns(Boolean) of the close_long and close_short methods in *strategy.py* .

### Final log outputs
Those outputs show the long/short close/tp/sl counter for each asset. Also shows Last balance , total fee , total operation counter. 
Those last outputs are very vital for real algo traders.

# Installation

Clone the repository with git:

*git clone https://github.com/denizyts/Backtester.git*

or just download the zip.

## Dependencies
Latest versions probably will be enough.

- *Python 3.11.8*
- *pandas 2.1.2*
- *pandas_ta 0.3.14*
- *numpy 1.26.0*
- *matplotlib 3.8.0*
- *binance.py 1.9.0* https://pypi.org/project/binance.py/


## Usage
*-python3 main.py*







