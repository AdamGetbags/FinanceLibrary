# -*- coding: utf-8 -*-
"""

@author: Adam Getbags
CoinGecko API: Advanced Guide

"""

#pip install pycoingecko

#import modules
import requests 
import pandas as pd
from pycoingecko import CoinGeckoAPI

#create a client
cg = CoinGeckoAPI()

#confirm connection
cg.ping()

#get a list of coins
coinList = cg.get_coins_list()
coinDataFrame = pd.DataFrame.from_dict(coinList).sort_values('id'
                                      ).reset_index(drop=True)

#btc/eth/dpx by id
#coinDataFrame[coinDataFrame['id'] == 'bitcoin']
#coinDataFrame[coinDataFrame['id'] == 'ethereum']
#coinDataFrame[coinDataFrame['id'] == 'dopex']
coins = ['bitcoin','ethereum','dopex']

#get list of suppored VS currencies
counterCurrencies = cg.get_supported_vs_currencies()
vsCurrencies = ['usd', 'eur', 'link']

#most simple price request - nested dictionary format
simplePriceRequest = cg.get_price(ids = coins, vs_currencies = 'usd')
print(simplePriceRequest)

complexPriceRequest = cg.get_price(ids = coins, 
                        vs_currencies = vsCurrencies, 
                        include_market_cap = True,
                        include_24hr_vol = True,
                        include_24hr_change = True,
                        include_last_updated_at = True)
print(complexPriceRequest)

#get all asset platforms
assetPlatformsList = cg.get_asset_platforms()
assetPlatforms = pd.DataFrame.from_dict(assetPlatformsList
                   ).sort_values('id').reset_index(drop=True)

#assetPlatforms[assetPlatforms['id'] == 'binance-smart-chain']
#get AVAX token price (using contract address) from BSC (asset platform)
cg.get_token_price(id = 'binance-smart-chain', 
                   contract_addresses = '0x1ce0c2827e2ef14d5c4f' +
                                        '29a091d735a204794041',
                   vs_currencies = 'usd')