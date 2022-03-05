# -*- coding: utf-8 -*-
"""
TD API Intraday Data
@author: https://github.com/alexgolec/tda-api
shout out to Part Time Larry!!!
"""

from tda import auth, client
import json
import pandas as pd
from datetime import datetime, date
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

#6 months of weekly candles
# r = c.get_price_history('XOM',
#         period = c.PriceHistory.Period.SIX_MONTHS,
#         period_type = c.PriceHistory.PeriodType.MONTH,
#         frequency = c.PriceHistory.Frequency.DAILY,
#         frequency_type = c.PriceHistory.FrequencyType.WEEKLY)

#20 years of daily candles
# r = c.get_price_history('XOM',
        # period = c.PriceHistory.Period.TWENTY_YEARS,
        # period_type = c.PriceHistory.PeriodType.YEAR,
        # frequency = c.PriceHistory.Frequency.DAILY,
        # frequency_type = c.PriceHistory.FrequencyType.DAILY,)


#3 months of daily candles
# r = c.get_price_history('XOM',
        # period = c.PriceHistory.Period.THREE_MONTHS,
        # period_type = c.PriceHistory.PeriodType.MONTH,
        # frequency = c.PriceHistory.Frequency.DAILY,
        # frequency_type = c.PriceHistory.FrequencyType.DAILY)

#10 days of 30 minute candles NO postmarket data 
# r = c.get_price_history('XOM',
#         period = c.PriceHistory.Period.TEN_DAYS,
#         period_type = c.PriceHistory.PeriodType.DAY,
#         frequency = c.PriceHistory.Frequency.EVERY_THIRTY_MINUTES,
#         frequency_type = c.PriceHistory.FrequencyType.MINUTE,
#         need_extended_hours_data = False)

#2 days of 5 minute candles WITH postmarket data
# r = c.get_price_history('XOM',
#         period = c.PriceHistory.Period.TWO_DAYS,
#         period_type = c.PriceHistory.PeriodType.DAY,
#         frequency = c.PriceHistory.Frequency.EVERY_FIVE_MINUTES,
#         frequency_type = c.PriceHistory.FrequencyType.MINUTE)

#2 days of 5 minute candles NO postmarket data 
# r = c.get_price_history('XOM',
#         period = c.PriceHistory.Period.TWO_DAYS,
        # period_type = c.PriceHistory.PeriodType.DAY,
        # frequency = c.PriceHistory.Frequency.EVERY_FIVE_MINUTES,
        # frequency_type = c.PriceHistory.FrequencyType.MINUTE,
        # need_extended_hours_data = False)

#datetime object
#dt = datetime(2019, 12,4)

# specific date range - in milliseconds since epoch 
r = c.get_price_history('XOM',
        start_datetime = datetime(2019, 12,4), 
        end_datetime = datetime(2020, 12,4),
        period_type = c.PriceHistory.PeriodType.YEAR,
        frequency = c.PriceHistory.Frequency.DAILY,
        frequency_type = c.PriceHistory.FrequencyType.DAILY,
        need_extended_hours_data = False) #datetime.today())


#JSON to dataframe
assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4))

#JSON to dataframe
data = pd.json_normalize(r.json(), record_path = ['candles'])

#format index
data['date'] = pd.to_datetime((data.datetime*1000000),
                              format = '%Y-%m-%d')#.dt.date

#set index
data = data.set_index('date')

#plot candlestick chart
mpf.plot(data[:], type = 'candle', mav = (10, 20, 50), volume = True)