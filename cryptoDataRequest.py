# -*- coding: utf-8 -*-
"""
crypto data request
@author: Adam Getbags
"""

#import modules
# import pandas as pd
from selenium import webdriver
from time import sleep
import os
import pandas as pd
from selenium.webdriver.common.by import By
from investingSecrets import username, pw

url = "https://www.investing.com/crypto/bitcoin/historical-data"

class timeSeriesGrabber:
    def __init__(self, url, username, pw):
        #open the historical data page
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        sleep(3)
        
        #click download data to bring up sign in 
        self.driver.find_element(By.XPATH,
            "//a[contains(text(), 'Download Data')]").click()
        sleep(3)
        #pass credentials
        self.driver.find_element(By.ID, "loginFormUser_email").send_keys(username)
        sleep(1)
        self.driver.find_element(By.ID, "loginForm_password").send_keys(pw)
        sleep(1)
        #click sign in
        self.driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/a").click()
        
        #scroll down
        self.driver.execute_script("window.scrollTo(0, 280)")
        sleep(2)
        
        #click into date panel
        self.driver.find_element(By.ID, "widgetField").click()
        sleep(1)
        
        #clear dates and send new dates
        self.driver.find_element(By.ID, "startDate").clear()
        sleep(.5)
        self.driver.find_element(By.ID, "startDate").send_keys("01/01/2008")
        sleep(.5)
        self.driver.find_element(By.ID, "endDate").clear()
        sleep(.5)
        self.driver.find_element(By.ID, "endDate").send_keys("01/01/2030")
        sleep(.5)
        
        #click apply button to update time series
        self.driver.find_element(By.ID, "applyBtn").click()
        sleep(7)
        self.driver.find_element(By.XPATH,
            "/html/body/div[5]/section/div[7]/div[2]/div[4]/div/a").click()
        
#get data
timeSeriesGrabber(url, username, pw)   

#read file into dataframe
timeSeries = pd.read_csv('C:\\Users\\AmatVictoriaCuramIII\\Downloads\\' +
           'Bitcoin Historical Data - Investing.com.csv')

#drop Change % column
timeSeries = timeSeries.drop("Change %", axis = 1)

#reformat date
timeSeries['Date'] = pd.to_datetime(timeSeries['Date'])

#set date column to be index
timeSeries = timeSeries.set_index('Date')

#rename column titles
timeSeries = timeSeries.rename(
             columns = {"Price":"Close", "Vol.":"Volume"}, errors = 'raise')

#remove commas from prices and dashes from volume
timeSeries.replace(",","", regex = True, inplace = True)
timeSeries.replace("-","0", regex = True, inplace = True)

#Remove K and M from volume data and move decimal point
for i in timeSeries['Volume'].index:
    if "K" in timeSeries.loc[i, 'Volume']:
        timeSeries.loc[i, 'Volume'] = float(timeSeries.loc[i, 'Volume'
                                        ].replace('K', '')) * 1000
    elif "M" in timeSeries.loc[i, 'Volume']:
        timeSeries.loc[i, 'Volume'] = float(timeSeries.loc[i, 'Volume'
                                        ].replace('M', '')) * 1000000
        
#convert to numeric data types
timeSeries[["Close", "Open", "High", "Low", "Volume"]] = timeSeries[[
            "Close", "Open", "High", "Low", "Volume"]].apply(pd.to_numeric)

print(timeSeries)