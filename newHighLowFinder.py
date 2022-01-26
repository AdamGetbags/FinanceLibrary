# -*- coding: utf-8 -*-
"""
SP500 Internals
@author: Adam Getbags
"""

#import modules
import pandas as pd 
import yahoo_fin.stock_info as si

#empty dataframe
sp500data = pd.DataFrame(columns = ('Ticker', 'New Low', 'New High'))

#n day high/low
n = 252

#in last t days
t = 5

tickers = pd.read_excel("Excel File Path Goes Here")
tickers['Symbol'] = tickers['Symbol'].replace('\.', '-', regex = True)


#ticker
# i = 'SNAP'

for i in tickers['Symbol'][:50]:

    #request data
    priceData = si.get_data(i)
    
    #n day high/low
    priceData['nDayLow'] = priceData['low'].rolling(n).min()
    priceData['nDayHigh'] = priceData['high'].rolling(n).max()
    
    #long form for checking new lows
    # for i in priceData[-t:].index:
    #     if priceData['low'][i] <= priceData['nDayLow'][i]:
    #         print('True')
    #     else:
    #         print('False')
    
    #list comprehension
    newLows = True in [True if priceData['low'][i] <= priceData['nDayLow'][i] else
                       False for i in priceData[-t:].index]
    
    newHighs = True in [True if priceData['high'][i] >= priceData['nDayHigh'][i] else
                        False for i in priceData[-t:].index]
    
    #append data to list
    dataList = [i, newLows, newHighs]
    print(dataList)
    
    #add list to Dataframe
    sp500data.loc[len(sp500data.index)] = dataList
    
#companies with n day lows/highs in last t days
companyListLows = [sp500data['Ticker'][i] for i in sp500data.index if
                   sp500data['New Low'][i] == True]
companyListHighs = [sp500data['Ticker'][i] for i in sp500data.index if
                   sp500data['New High'][i] == True]

#number of companies with n day lows/high in last t days
numLows = len(companyListLows)
print(str(numLows) + " companies with {} trading day lows in last {} days.".format(n, t))
numHighs = len(companyListHighs)
print(str(numHighs) + " companies with {} trading day lows in last {} days.".format(n, t))

#percent of sp500 with n day lows/highs in last t days 
percentLows = numLows / len(sp500data['New Low'])
print("{:.2%}".format(percentLows) + 
      " of the sp500 has had {} trading day low in last {} days.".format(n, t))
percentHighs = numHighs / len(sp500data['New High'])
print("{:.2%}".format(percentLows) + 
      " of the sp500 has had {} trading day low in last {} days.".format(n, t))
