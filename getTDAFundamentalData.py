# -*- coding: utf-8 -*-
"""
TD API Get Fundamental Data
@author: https://github.com/alexgolec/tda-api
shout out to Part Time Larry!
"""

#import modules
from tda import auth, client
import json
import pandas as pd
from datetime import datetime
import TDAsecrets


#authentication flow
try:
    c = auth.client_from_token_file(TDAsecrets.token_path, TDAsecrets.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, TDAsecrets.api_key, TDAsecrets.redirect_uri,
            TDAsecrets.token_path)

#get ticker info
# r = c.get_quote('XOM')

#get fundamental data
r = c.search_instruments(['XOM','PBF','AAPL','MUR'], c.Instrument.Projection.FUNDAMENTAL)

assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4))

#empty DataFrame
data = pd.DataFrame()

#for each ticker in json, add to dataframe
for i in r.json():
    data = pd.concat([data,pd.DataFrame(pd.json_normalize(r.json()[i]))])
    
#get old columns
oldColumns = data.columns 

#rename columns
newColumns = [i.replace('fundamental.','') for i in list(data.columns)]

#create column mappings 
columnDict = {i:j for i,j in zip(oldColumns,newColumns)}

#rename column titles
data = data.rename(columns = columnDict)
