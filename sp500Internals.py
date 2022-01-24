# -*- coding: utf-8 -*-
"""
SP500 Internals
@author: Adam Getbags
"""

#Import modules
import pandas as pd
import yahoo_fin.stock_info as si

#empty dataframe
sp500data = pd.DataFrame(columns = ("Ticker", "New Low"))

#n day lows
n = 252
#in last t days
t = 5

#get list of tickers
tickers = pd.read_excel("/Users/amatvictoriacuramiv/Desktop/tickers.xlsx")
tickers['Symbol'] = tickers['Symbol'].replace("\.","-",regex=True)

#ticker 
# i = "SNAP"

#for loop
for i in tickers['Symbol'][:50]: 
    
    #ticker
    # print(i)
    
    #request data
    priceData = si.get_data(i)
    priceData['nDayLow'] = priceData['low'].rolling(n).min()
    
    #long form 
    # for i in priceData[-5:].index:
    #     if priceData['52wkLow'][i] == priceData['low'][i]:
    #         print("True")
    #     else: 
    #         print("False")
            
    #list comprehension - new lows in past n days
    newLows = True in [True if priceData['low'][i] <= priceData['nDayLow'][i] else 
                       False for i in priceData[-t:].index]
    
    #list to append to dataframe
    dataList = [i, newLows]
    print(dataList)
    
    sp500data.loc[len(sp500data.index)] = dataList
    
#companies with n day lows in last t days    
companyList = [sp500data['Ticker'][i] for i in sp500data.index if 
               sp500data['New Low'][i] == True]
print(companyList)

#number of companies with n day lows in last t days  
numLows = sp500data['New Low'].sum()
print(str(numLows) + " companies with {} trading day lows in last {} days.".format(n, t))

#percentage of sp500 with n day lows in last t days  
percentLows = numLows/len(sp500data['New Low'])
print("{:.2%}".format(percentLows) + 
      " of the sp500 has had {} trading day low in last {} days.".format(n, t))