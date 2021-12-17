# -*- coding: utf-8 -*-
"""
Get Calendar Spread Price
@author: Adam Getbags
"""

#import modules
import pandas as pd
from yahoo_fin import options as op

def getCalendarSpreadPrice(ticker, spreadType, longExpNo, shortExpNo, strike):
    
#inputs
# ticker = 'PLTR'
# spreadType = 'put' #call or put
# longExpNo = 7
# shortExpNo = 5
# strike = 19

    try:
    
        #get expiration dates
        expirationDates = op.get_expiration_dates(ticker)
        
        print('- - - Getting Data - - -\n')
        
        #get data based on spread type, call or put spread
        if spreadType == 'call':
            longChainData = op.get_calls(ticker, date = expirationDates[longExpNo])
            shortChainData = op.get_calls(ticker, date = expirationDates[shortExpNo])
        elif spreadType == 'put':
            longChainData = op.get_puts(ticker, date = expirationDates[longExpNo])
            shortChainData = op.get_puts(ticker, date = expirationDates[shortExpNo])
        else: 
            print('Please enter call or put for spreadType.')
            return
        
        #trim data 
        longChainData = longChainData[['Strike', 'Bid', 'Ask', 'Last Price']][
            longChainData['Strike'] == strike]
        shortChainData = shortChainData[['Strike', 'Bid', 'Ask', 'Last Price']][
            shortChainData['Strike'] == strike]
        
        #reset index
        longChainData = longChainData.reset_index(drop = True)
        shortChainData = shortChainData.reset_index(drop = True)
        
        #change to numeric data type
        longChainData['Strike'] = pd.to_numeric(
                longChainData['Strike'], errors = 'coerce')
        longChainData['Bid'] = pd.to_numeric(
                longChainData['Bid'], errors = 'coerce')
        longChainData['Ask'] = pd.to_numeric(
                longChainData['Ask'], errors = 'coerce')
        longChainData['Last Price'] = pd.to_numeric(
                longChainData['Last Price'], errors = 'coerce')
        
        shortChainData['Strike'] = pd.to_numeric(
                shortChainData['Strike'], errors = 'coerce')
        shortChainData['Bid'] = pd.to_numeric(
                shortChainData['Bid'], errors = 'coerce')
        shortChainData['Ask'] = pd.to_numeric(
                shortChainData['Ask'], errors = 'coerce')
        shortChainData['Last Price'] = pd.to_numeric(
                shortChainData['Last Price'], errors = 'coerce')
        
        #create mid price for reference
        longChainData['Mid'] = (longChainData['Bid'] + longChainData['Ask']) / 2
        shortChainData['Mid'] = (shortChainData['Bid'] + shortChainData['Ask']) / 2
        
        print('Long Chain Data')
        print('')
        print(longChainData, '\n - - - - - - - - -')
        print('Short Chain Data')
        print('')
        print(shortChainData, ' \n')
        
        #get spread price
        spreadPrice = longChainData['Ask'].iloc[0] - shortChainData['Bid'].iloc[0]
        
        #print pricing
        if spreadType == 'call' and shortExpNo < longExpNo:
            print('Long Call Calendar Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'call' and shortExpNo > longExpNo:
            print('Short Call Calendar Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif spreadType == 'put' and longExpNo > shortExpNo:
            print('Long Put Calendar Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'put' and longExpNo < shortExpNo:
            print('Short Put Calendar Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif longExpNo == shortExpNo:
            print('Strike prices are the same, no vertical spreads here.')
            return

        #output
        return  round(spreadPrice, 4)
    
    except IndexError:
        print('Strike data not available, try again.')
