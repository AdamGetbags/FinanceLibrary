# -*- coding: utf-8 -*-
"""
TD API Access
@author: https://github.com/alexgolec/tda-api
shout out to Part Time Larry!!!
"""

from tda import auth, client
import json
import pandas as pd
from datetime import datetime
import TDAsecrets

try:
    c = auth.client_from_token_file(TDAsecrets.token_path, TDAsecrets.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, TDAsecrets.api_key, TDAsecrets.redirect_uri,
            TDAsecrets.token_path)

r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)

assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4))

data = pd.json_normalize(r.json(), record_path = ['candles'])

data['date'] = pd.to_datetime((data.datetime*1000000),
                              format = '%Y-%m-%d').dt.date

data = data.set_index('date')
data.close[-1000:].plot()