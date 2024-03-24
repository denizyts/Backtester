import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime as dt

def draw(wallet_value_list):

 #for i in range(len(timelist)):
  #timelist[a_coin_name][i] = dt.fromtimestamp(timelist[a_coin_name][i]/1000)

 plt.plot(wallet_value_list )

 plt.show()
