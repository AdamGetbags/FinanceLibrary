# -*- coding: utf-8 -*-
"""
TD API Candlestick Charts
@author: https://github.com/alexgolec/tda-api
shout out to Part Time Larry!!!
"""

#import modules
from tda import auth, client
import json
import pandas as pd
from datetime import datetime
import TDAsecrets
import mplfinance as mpf #pip install mplfinance

#authentication flow
try:
    c = auth.client_from_token_file(TDAsecrets.token_path, TDAsecrets.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, TDAsecrets.api_key, TDAsecrets.redirect_uri,
            TDAsecrets.token_path)

#request data
r = c.get_price_history('XOM',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)

#print JSON data
assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4))

#JSON to datafame
data = pd.json_normalize(r.json(), record_path = ['candles'])

#format date 
data['date'] = pd.to_datetime((data.datetime*1000000),
                              format = '%Y-%m-%d')#.dt.date

#set index to pandas datetimeindex
data = data.set_index('date')

#plot candlestick chart
mpf.plot(data[-100:], type = 'candle', mav = (10, 20, 50), volume = True)