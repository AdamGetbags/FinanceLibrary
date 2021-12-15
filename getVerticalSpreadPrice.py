# -*- coding: utf-8 -*-
"""
Get Vertical SpreadPrice
@author: Adam Getbags
"""

#import modules
import pandas as pd
from yahoo_fin import options as op

def getVerticalSpreadPrice(ticker, spreadType, expNo, longStrike, shortStrike):
    
# #inputs
# ticker = 'PLTR'
# spreadType = 'put' #call or put
# expNo = 5
# longStrike = 20
# shortStrike = 19

    try:
    
        #get expiration dates
        expirationDates = op.get_expiration_dates(ticker)
        
        print('- - - Getting Data - - -\n')
        
        #get data based on spread type, call or put spread
        if spreadType == 'call':
            chainData = op.get_calls(ticker, date = expirationDates[expNo])
        elif spreadType == 'put':
            chainData = op.get_puts(ticker, date = expirationDates[expNo])
        else: 
            print('Please enter call or put for spreadType.')
            return
        
        #trim data 
        chainData = chainData[['Strike', 'Bid', 'Ask', 'Last Price']][
            (chainData['Strike'] == longStrike) |
            (chainData['Strike'] == shortStrike)]
        
        #reset index
        chainData = chainData.reset_index(drop = True)
        
        #change to numeric data type
        chainData['Strike'] = pd.to_numeric(
                chainData['Strike'], errors = 'coerce')
        chainData['Bid'] = pd.to_numeric(
                chainData['Bid'], errors = 'coerce')
        chainData['Ask'] = pd.to_numeric(
                chainData['Ask'], errors = 'coerce')
        chainData['Last Price'] = pd.to_numeric(
                chainData['Last Price'], errors = 'coerce')
        
        #create mid price for reference
        chainData['Mid'] = (chainData['Bid'] + chainData['Ask']) / 2
        
        print(chainData)
        print('')
        
        #get spread price
        spreadPrice = chainData['Ask'][chainData['Strike'] == longStrike].iloc[0
                  ] - chainData['Bid'][chainData['Strike'] == shortStrike].iloc[0]
        
        #print pricing
        if spreadType == 'call' and longStrike < shortStrike:
            print('Long Call Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'call' and longStrike > shortStrike:
            print('Short Call Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif spreadType == 'put' and longStrike > shortStrike:
            print('Long Put Spread Price is $' + str(round(spreadPrice, 4)))
        elif spreadType == 'put' and longStrike < shortStrike:
            print('Short Put Spread Price is -$' + str(abs(round(spreadPrice, 4))))
        elif longStrike == shortStrike:
            print('Strike prices are the same, no vertical spreads here.')
            return
            
        #output
        return  round(spreadPrice, 4)
    
    except IndexError:
        print('Strike data not available, try again.')
