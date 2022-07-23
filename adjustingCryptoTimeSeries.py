# -*- coding: utf-8 -*-
"""

Adjust crypto prices for stock price time series analysis
@author: adam getbags

"""

#import modules
import yahoo_fin.stock_info as si
from pycoingecko import CoinGeckoAPI
import pandas as pd
import numpy as np
import datetime as dt

#create a client
cg = CoinGeckoAPI()

#confirm connection
cg.ping()

#get equity data
eqData = si.get_data("^GSPC", start_date = "01/01/2010",
                                  end_date = "01/01/2023") 

#get crypto data daily historical data
cryptoRequest = cg.get_coin_market_chart_by_id(id = 'bitcoin', 
                               vs_currency = 'usd',
                               days = 'max')

#list of lists to dataframe 
cryptoData = pd.DataFrame(data = cryptoRequest['prices'],
                                        columns = ['Date', 'Price'])
#reformat date
cryptoData['Date'] = cryptoData['Date'].apply(
                                        lambda x: pd.to_datetime(x*1000000))
#set index
cryptoData = cryptoData.set_index('Date')

#plot
cryptoData['Volume'] = [j for i, j in cryptoRequest['total_volumes']]

#review indexes to align 'close' prices
eqData['close']
cryptoData['Price']

#join
allData = pd.DataFrame(eqData['close']).join(cryptoData['Price'].shift(-1))
allData = allData.rename(columns = {'close':'eqClose', 'Price':'cryptoClose'})

#get first valid index to trim data
trimSpot = allData['cryptoClose'].first_valid_index()

#verify
allData['cryptoClose'][820:].head(50)

#trim data set
allData = allData.truncate(before = trimSpot)

#check for nans
allData.isnull().values.any()

#forward fill nans 
allData['cryptoClose'] = allData['cryptoClose'].fillna(method = 'ffill')


allData['eqLogReturns'] = np.log(allData.eqClose/allData.eqClose.shift(1))

allData['cryptoLogReturns'] = np.log(
                          allData.cryptoClose/allData.cryptoClose.shift(1))

#trim first row with nans
allData = allData[1:]