# -*- coding: utf-8 -*-
"""

@author: Adam Getbags
Equity Correlation Matrix

"""

#Import modules
import yahoo_fin.stock_info as si
import numpy as np
import pandas as pd

#assign start/end dates
startDate = "01/01/1960"
endDate = "01/01/2030"

#assign minimum time series length
minLength = 9**9 

#dataframe to store returns
returns = pd.DataFrame()

#assign tickers
tickers = ['SPY','^RUT','TLT','GLD','SLV', 'WEAT','SOYB','JO']

#request and save data
#for each ticker in list 
for t in tickers:
    #request data
    ts = si.get_data(t, start_date = startDate, end_date = endDate)
    #calculate log returns
    ts['LogRet'] = np.log(ts['adjclose']/ts['adjclose'].shift(1))
    #save to .xlsx in a folder
    ts.to_excel('C:/Users/AmatVictoriaCuramIII/Desktop/The Folder/' + 
              'timeSeriesData/' + t + '.xlsx', index_label = 'dateIndex')
    print('Data returned for '+ t)

#for each ticker in list
for t in tickers:
    #read .xlsx file into variable
    ts = pd.read_excel('C:/Users/AmatVictoriaCuramIII/Desktop/The Folder/' + 
              'timeSeriesData/' + t + '.xlsx')
    #set index to date instead of integer range
    ts = ts.set_index('dateIndex')
    #append log returns column to the returns dataframe
    returns = pd.concat([returns,ts['LogRet']],axis = 1)
    
    #check time series length to trim log returns for correlation 
    if len(ts) < minLength:
        minLength = len(ts)
    else:
        pass
    
#rename columns
returns.columns = tickers
#trim time series
returns = returns[-(minLength-1):]
#create correlation matrix
matrix = returns.corr()

#display dataframes
print(matrix)
#sort to find highest/lowest correlation time series
print(matrix['SPY'].sort_values(ascending = True))

#rolling correlation graph
returns['SPY'].rolling(20).corr(returns['GLD']).plot()