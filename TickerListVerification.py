# -*- coding: utf-8 -*-
"""

@author: AdamGetbags

"""

#Import modules
import requests
import pandas as pd
import os 
import yahoo_fin.stock_info as si
import time as t
from socket import gaierror
from json import JSONDecodeError

#Define function
def validateTickers():
    #Create emtpy list to store tickers
    validTickersList = []
    #Load tickers into .xlsx
    excelFile = pd.read_excel('TickerList.xlsx')
    #Create Series with only tickers
    Tickers = excelFile['Symbol'].astype(str)
    
    #For loop to confirm if ticker has data
    for ticker in Tickers[:]:
        #Request throttle 
        t.sleep(1)
        #Try to request and save data
        try: 
            #See if recent daily OHLC data is available for a short window
            tempVar = si.get_data(ticker, start_date = "08/01/2021",
                                  end_date = "01/01/2022") 
            #If available, save ticker 
            validTickersList.append(ticker)
            #Print notice
            print(ticker + " confirmed")
        #Exceptions for invalid ticker   
        except AssertionError: 
            #Print notice
            print("Invalid ticker for " + ticker + " : AssertionError")
            #Continue to next ticker
            continue
        #Exceptions for invalid timestamps
        except KeyError: 
            #Print notice
            print("Timestamp error for " + ticker + " : KeyError")
            #Continue to next ticker
            continue
        #Exception for JSON Decode error
        except JSONDecodeError:
            try:
                #Print notice
                print("JSON Decode error for " + ticker + ", sleeping for 30s")
                #Sleep
                t.sleep(31)
                #See if recent daily OHLC data is available for a short window
                tempVar = si.get_data(ticker, start_date = "08/01/2021",
                                      end_date = "01/01/2022") 
                #If available, save ticker 
                validTickersList.append(ticker)
                #Print notice
                print(ticker + " confirmed")
            #Second JSON Decode Error, after sleeping
            except JSONDecodeError:
                #Print notice
                print('Second JSON Decode error for ' + ticker)
                continue
            #Exceptions for invalid ticker   
            except AssertionError: 
                #Print notice
                print("Invalid ticker for " + ticker + " : AssertionError")
                #Continue to next ticker
                continue
            #Exceptions for invalid timestamps
            except KeyError: 
                #Print notice
                print("Timestamp error for " + ticker + " : KeyError")
                #Continue to next ticker
                continue
        #Exception for Get Address Info error
        except gaierror:
            try:
                #Print notice
                print("GAI error for " + ticker + " - sleeping 5 mins")
                #Sleep
                t.sleep(301)
                #See if recent daily OHLC data is available for a short window
                tempVar = si.get_data(ticker, start_date = "08/01/2021",
                                      end_date = "01/01/2022") 
                #If available, save ticker 
                validTickersList.append(ticker)
                #Print notice
                print(ticker + " confirmed")
            #Second Connection Error, after sleeping
            except gaierror:
                #Print notice
                print('Second GIA error for ' + ticker + " - sleeping 5 mins")
                #Sleep 
                t.sleep(301)
                continue
    #List to dataframe
    validTickersDataframe = pd.DataFrame(validTickersList, columns = ['Symbol'])
    #Save validated tickers to .xlsx    
    validTickersDataframe.to_excel('validTickers.xlsx', index = False)
    pass
    
#Start timer
startTime = t.time()

validateTickers()

#End timer
endTime = t.time()    
#Print time
print(str(endTime - startTime) + ' seconds')