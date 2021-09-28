# -*- coding: utf-8 -*-
"""

@author: Adam Getbags

"""

#Import modules
import time as t
import pandas as pd
import yahoo_fin.stock_info as si
from datetime import datetime

#Start timer
startTime = t.time()
#Import tickers from excel file
tickers = pd.read_excel('validTickers.xlsx')

#Empty list
divYieldList = []

#Define function
def getDividendStocks():
    #For all stocks in list
    for i in tickers["Symbol"][:]:
        try:
            #Ticker to pull data for 
            ticker = i
            #Try block for all exception issues during requests
            try:
                #Request data sets
                priceData = si.get_data(ticker)
                #Sleep 
                # t.sleep(1)
                dividendData = si.get_dividends(ticker)
            except:
                print('No dice. Skipping ' + ticker)
                continue

            #If there is no dividend data continue to next ticker
            if len(dividendData) == 0:
                print("No dividend data for " + ticker)
                continue 

            #Get last price
            lastPrice = priceData["adjclose"][-1]
            #Get last dividend
            lastDividend = dividendData["dividend"][-1]
            #Calculate dividend yield IN PERCENT
            divYield = ((lastDividend / lastPrice) * 100).round(5)

            #Get last dividend date
            lastDivDate = datetime.fromtimestamp(dividendData.index[-1].timestamp())
            #Get dividend before last date
            secondLastDivDate = datetime.fromtimestamp(dividendData.index[-2].timestamp())
            #Days between last dividends
            dateDifference = (lastDivDate - secondLastDivDate).days

            #If hasn't paid dividend in last 385 days, continue
            if (datetime.now() - lastDivDate).days > 385:
                continue

            #Estimate dividend frequency
            if dateDifference < 120:
                divFrequency = "Quarterly"
            elif dateDifference < 210:
                divFrequency = "SemiAnnual"
            elif dateDifference < 385:
                divFrequency = "Annual"
            elif dateDifference > 385:
                divFrequency = "Irregular"

            #Add items to temporary list
            tempList = [ticker, divYield, divFrequency, 
                        str(lastDivDate.date()), dateDifference]
            #Add temporary list to master list
            divYieldList.append(tempList)

            #Print notice
            print(ticker + " confirmed")

            #Sleep
            # t.sleep(1)
        except IndexError:
            print("Index Error - not enough data")
            continue
    #Turn master list into DataFrame
    divYieldData = pd.DataFrame(divYieldList, columns = [
        "Ticker", "DivYield", "Frequency", "PreviousDivDate", "DivDateDiff"])

    divYieldData = divYieldData.sort_values(by = ["DivYield"], ascending = False)

    #Export dividend yield info into excel
    divYieldData.to_excel("DividendYieldData.xlsx", index = False)

    #End time
    endTime = t.time()
    #Print time for program to run
    print('Dividend analysis took ' + str(endTime - startTime) + " seconds.")
    
getDividendStocks()    
