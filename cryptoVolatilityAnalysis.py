# -*- coding: utf-8 -*-
"""

Crypto Historical Volatility Analysis
@author: Adam Getbags

"""

#Import modules
import yahoo_fin.stock_info as si
import numpy as np
from investingCredentials import username, pw
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd

# from btcFilePath import btcFilePath
btcFilePath = "C:/Users/AmatVictoriaCuramIII/Downloads/BTCUSD.csv"

# #url to scrape
# url = "https://www.investing.com/crypto/bitcoin/historical-data"

# #create class for bot
# class timeSeriesGrabber:
#     def __init__(self, url, username, pw):
#         #open the historical data page
#         self.driver = webdriver.Chrome()
#         self.driver.get(url)
#         sleep(4)
        
#         #click download data to bring up sign in
#         self.driver.find_element(By.XPATH,
#              "//a[contains(text(), 'Download Data')]").click()
#         sleep(2)
        
#         #send credentials into input boxes
#         self.driver.find_element(By.ID, "loginFormUser_email").send_keys(username)
#         sleep(1)
#         self.driver.find_element(By.ID, "loginForm_password").send_keys(pw)
#         sleep(1)
        
#         #click sign in button
#         self.driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/a").click()
#         sleep(1)
        
#         #scroll down
#         self.driver.execute_script("window.scrollTo(0, 280)")
#         sleep(2)
#         #click into date panel
#         self.driver.find_element(By.ID, "widgetField").click()
        
#         #clear dates and send new ones
#         self.driver.find_element(By.ID, "startDate").clear()
#         sleep(.5)
#         self.driver.find_element(By.ID, "startDate").send_keys('01/01/2008')
#         sleep(.5)
#         self.driver.find_element(By.ID, "endDate").clear()
#         sleep(.5)
#         self.driver.find_element(By.ID, "endDate").send_keys('01/01/2030')
        
#         #click apply
#         self.driver.find_element(By.ID, "applyBtn").click()
#         sleep(7)
        
#         #download data
#         self.driver.find_element(By.XPATH,
#             "/html/body/div[5]/section/div[7]/div[2]/div[4]/div/a").click()
#         sleep(7)
        
#run it        
# timeSeriesGrabber(url, username, pw)

#read csv to dataframe
timeSeries = pd.read_csv(btcFilePath)

#drop Change % column
timeSeries = timeSeries.drop("Change %", axis = 1)

#reformat date
timeSeries['Date'] = pd.to_datetime(timeSeries['Date'])

#set index to date column
timeSeries = timeSeries.set_index('Date')

#rename Price to Close and Vol. to Volume
timeSeries = timeSeries.rename(
              columns = {"Price":"Close", "Vol.":"Volume"}, errors = "raise")

#remove commas from prices and dashes from volume
timeSeries.replace(",","", regex = True, inplace = True)
timeSeries.replace("-","0", regex = True, inplace = True)

#remove K and M from volume data and move decimal point
for i in timeSeries['Volume'].index:
    if "K" in timeSeries.loc[i, 'Volume']:
        timeSeries.loc[i, 'Volume'] = float(timeSeries.loc[i, 'Volume'
                                            ].replace('K','')) * 1000
    elif "M" in timeSeries.loc[i, 'Volume']:
        timeSeries.loc[i, 'Volume'] = float(timeSeries.loc[i, 'Volume'
                                            ].replace('M','')) * 1000000
    elif "B" in timeSeries.loc[i, 'Volume']:
        timeSeries.loc[i, 'Volume'] = float(timeSeries.loc[i, 'Volume'
                                            ].replace('B','')) * 1000000000    
        
#convert to numeric data type
timeSeries[['Close', 'Open', 'High', 'Low', 'Volume']] = timeSeries[[
            'Close', 'Open', 'High', 'Low', 'Volume']].apply(pd.to_numeric)

ts = timeSeries
#reordering df
ts = timeSeries.reindex(index=ts.index[::-1])

#daily log returns
ts['logRet'] = np.log(ts['Close']/ts['Close'].shift(1)) 
ts['logRet'] = ts['logRet'].fillna(0)

#price adjusted daily candle height - as a percent of price
ts['normalizedCandleHeight'] = (ts['High'] - ts['Low']) / ts['Close']

#min/max range in points
ts['allTimeLow'] = ts['Low'].min()
ts['allTimeHigh'] = ts['High'].max()

#percentage off ATH; AKA ATH drawdown
ts['pointsOffATH'] = ts['allTimeHigh'] - ts['Close']
ts['percentOffATH'] = ts['pointsOffATH'] / ts['allTimeHigh']

#plot
# ts['percentOffATH'].plot()

#rolling high/low range
rollingHighLowWindow = 20
ts['rollingLow'] = ts['Low'].rolling(rollingHighLowWindow).min()
ts['rollingHigh'] = ts['High'].rolling(rollingHighLowWindow).max()

#rolling high/low range over current price AKA price adjusted range
#can be > 1 if downtrending
#can't be > 1 if at all time high or uptrending
#thus, trend is important consideration
ts['rangeOverPrice'] = (
    ts['rollingHigh'] - ts['rollingLow']) / ts['Close']

#plot 
# ts['rangeOverPrice'].plot()

#log return Z Score
ts['avgLogReturn'] = ts['logRet'].mean()
ts['logReturnStdDev'] = ts['logRet'].std()
ts['logRetZScore'] = (
    ts['logRet'] - ts['avgLogReturn']) / ts['logReturnStdDev']

#plot
# ts['logRetZScore'].plot()

#candle height Z Score
#note, ts['normalizedCandleHeight'] and ts['candleHeightZScore'] have
#high correlation, but z score allows for comparability between time series
ts['avgCandleHeight'] = ts['normalizedCandleHeight'].mean()
ts['candleHeightStdDev'] = ts['normalizedCandleHeight'].std()
ts['candleHeightZScore'] = (
    ts['normalizedCandleHeight'] - ts['avgCandleHeight']
    ) / ts['candleHeightStdDev']

#plot
# ts['candleHeightZScore'].plot()

#rolling avg/stdDev window
rollingAvgStdDevWindow = 20

#rolling average log returns
ts['rollingAvgLogReturn'] = ts['logRet'].rolling(
    center=False, window = rollingAvgStdDevWindow).mean()

#plot
# ts['rollingAvgLogReturn'].plot()

#rolling stdDev log returns 
ts['rollingStdDevLogReturn'] = ts['logRet'].rolling(
    center=False, window = rollingAvgStdDevWindow).std()

#plot
# ts['rollingStdDevLogReturn'].plot()

#quantiles for rolling average log returns
ts['rollingAvgLogReturn'].quantile(q=0.01, interpolation='nearest')

#rate of change window
rocWindow = 20
#rolling rate of change 
ts['rateOfChange'] = (ts['Close'] - ts['Close'].shift(rocWindow)
                                  ) / ts['Close'].shift(rocWindow)  
ts['rateOfChange'] = ts['rateOfChange'].fillna(0)

# ts['rateOfChange'].plot()

#ATR Setup
avgTrueRangeWindow = 20
ts['Method1'] = ts['High'] - ts['Low']
ts['Method2'] = abs((ts['High'] - ts['Close'].shift(1)))
ts['Method3'] = abs((ts['Low'] - ts['Close'].shift(1)))
ts['Method1'] = ts['Method1'].fillna(0)
ts['Method2'] = ts['Method2'].fillna(0)
ts['Method3'] = ts['Method3'].fillna(0)
ts['TrueRange'] = ts[['Method1','Method2','Method3']].max(axis = 1)

ts['avgTrueRangePoints'] = ts['TrueRange'].rolling(
                      window = avgTrueRangeWindow, center=False).mean()    

# ts['avgTrueRangePoints'].plot()
    
ts['avgTrueRangePercent'] = ts['avgTrueRangePoints'] / ts['Close']
 
# ts['avgTrueRangePercent'].plot()

#efficiency = rate of change / ATR in points 
#high absolute values suggest larger moves, in a ~straight~ line
#ATR is in points to adjust for price 
ts['ROCefficiency'] = ts['Close'] - ts['Close'].shift(rocWindow)
ts['efficiency'] = ts['ROCefficiency'] / ts['avgTrueRangePoints'] 

# ts['efficiency'].plot()

#subset for correlation matrix
corrMat = ts[['efficiency','avgTrueRangePercent','avgTrueRangePoints',
              'TrueRange','rateOfChange','rollingStdDevLogReturn',
              'rollingAvgLogReturn','candleHeightZScore','logRetZScore',
              'rangeOverPrice','percentOffATH',]][20:].corr()