# -*- coding: utf-8 -*-
"""

Equity Historical Volatility Analysis
@author: Adam Getbags

"""

#Import modules
import yahoo_fin.stock_info as si
import numpy as np

#assign ticker
ticker = "PBF"

#assign start/end dates
startDate = "01/01/1960"
endDate = "01/01/2030"

#request time series data
ts = si.get_data(ticker, start_date = startDate, end_date = endDate)

#daily log returns
ts['logRet'] = np.log(ts['adjclose']/ts['adjclose'].shift(1)) 
ts['logRet'] = ts['logRet'].fillna(0)

#adjustmentRatio
ts['adjustmentRatio'] = ts['adjclose']/ts['close']

#adjusted OHL prices
ts['adjOpen'] = ts['open'] * ts['adjustmentRatio']
ts['adjLow'] = ts['low'] * ts['adjustmentRatio']
ts['adjHigh'] = ts['high'] * ts['adjustmentRatio']

#price adjusted daily candle height
ts['normalizedCandleHeight'] = (ts['adjHigh'] - ts['adjLow']) / ts['adjclose']

#min/max range in points
ts['adjAllTimeLow'] = ts['adjLow'].min()
ts['adjAllTimeHigh'] = ts['adjHigh'].max()

#percentage off ATH; AKA ATH drawdown
ts['pointsOffATH'] = ts['adjAllTimeHigh'] - ts['adjclose']
ts['percentOffATH'] = ts['pointsOffATH'] / ts['adjAllTimeHigh']

#plot
# ts['percentOffATH'].plot()

#rolling high/low range
rollingHighLowWindow = 20
ts['adjRollingLow'] = ts['adjLow'].rolling(rollingHighLowWindow).min()
ts['adjRollingHigh'] = ts['adjHigh'].rolling(rollingHighLowWindow).max()

#rolling high/low range over current price AKA price adjusted range
#can be > 1 if downtrending
#can't be > 1 if at all time high or uptrending
#thus, trend is important consideration
ts['rangeOverPrice'] = (
    ts['adjRollingHigh'] - ts['adjRollingLow']) / ts['adjclose']

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
ts['rateOfChange'] = (ts['adjclose'] - ts['adjclose'].shift(rocWindow)
                                  ) / ts['adjclose'].shift(rocWindow)  
ts['rateOfChange'] = ts['rateOfChange'].fillna(0)

# ts['rateOfChange'].plot()

#ATR Setup
avgTrueRangeWindow = 20
ts['Method1'] = ts['adjHigh'] - ts['adjLow']
ts['Method2'] = abs((ts['adjHigh'] - ts['adjclose'].shift(1)))
ts['Method3'] = abs((ts['adjLow'] - ts['adjclose'].shift(1)))
ts['Method1'] = ts['Method1'].fillna(0)
ts['Method2'] = ts['Method2'].fillna(0)
ts['Method3'] = ts['Method3'].fillna(0)
ts['TrueRange'] = ts[['Method1','Method2','Method3']].max(axis = 1)

ts['avgTrueRangePoints'] = ts['TrueRange'].rolling(
                     window = avgTrueRangeWindow, center=False).mean()    

# ts['avgTrueRangePoints'].plot()
    
ts['avgTrueRangePercent'] = ts['avgTrueRangePoints'] / ts['adjclose']
 
# ts['avgTrueRangePercent'].plot()

#efficiency = rate of change / ATR in points 
#high absolute values suggest larger moves, in a ~straight~ line
#ATR is in points to adjust for price 
ts['ROCefficiency'] = ts['adjclose'] - ts['adjclose'].shift(rocWindow)
ts['efficiency'] = ts['ROCefficiency'] / ts['avgTrueRangePoints'] 

# ts['efficiency'].plot()

#subset for correlation matrix
corrMat = ts[['efficiency','avgTrueRangePercent','avgTrueRangePoints',
              'TrueRange','rateOfChange','rollingStdDevLogReturn',
              'rollingAvgLogReturn','candleHeightZScore','logRetZScore',
              'rangeOverPrice','percentOffATH',]][20:].corr()