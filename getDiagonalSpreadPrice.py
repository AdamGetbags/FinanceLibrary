# -*- coding: utf-8 -*-
"""
Get Diagonal Spread Price
@author: Adam Getbags
"""

#import modules
import pandas as pd
from yahoo_fin import options as op

def getDiagonalSpreadPrice(ticker, spreadType, longExpNo, shortExpNo,
                            longStrike, shortStrike):
    
# #inputs
# ticker = 'PLTR'
# spreadType = 'put' #call or put
# longExpNo = 7
# shortExpNo = 5
# longStrike = 20
# shortStrike = 19

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
            longChainData['Strike'] == longStrike]
        shortChainData = shortChainData[['Strike', 'Bid', 'Ask', 'Last Price']][
            shortChainData['Strike'] == shortStrike]
        
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
        
        #add expiration to dataframe
        longChainData['Expiration'] = expirationDates[longExpNo]
        shortChainData['Expiration'] = expirationDates[shortExpNo]
        
        print('Long Chain Data')
        print('')
        print(longChainData, '\n - - - - - - - - -')
        print('Short Chain Data')
        print('')
        print(shortChainData, ' \n')
        
        #get spread price
        spreadPrice = longChainData['Ask'].iloc[0] - shortChainData['Bid'].iloc[0]
        
        #print pricing
        if spreadType == 'call' and spreadPrice > 0:
            print('Long Call Diagonal Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'call' and spreadPrice < 0:
            print('Short Call Diagonal Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif spreadType == 'put' and spreadPrice > 0:
            print('Long Put Diagonal Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'put' and spreadPrice < 0:
            print('Short Put Diagonal Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif longExpNo == shortExpNo and shortStrike == longStrike:
            print('Strike prices are the same, no diagonal spreads here.')
            return

        #output
        return round(spreadPrice, 4)
    
    except IndexError:
        print('Strike data not available, try again.')
