#BY: Mohammad Sabir Khan

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf
from yahoo_fin import stock_info as si
import pandas_datareader as datareader
import pandas_datareader.data as web
import requests as req
%matplotlib inline

####################################################################
#PURPOSE: to return the date in a format recognized by the dataframe
#ARGS: n/a
#RETURNS: string
#NOTE: Currently, this should only run when market is closed
#TO-DO: Add functionality that will get hour by hour data
####################################################################
def get_date(date='today'):
    #if no specific date is entered
    if(date == 'today'):
         #check if today is sunday
        if(datetime.date(datetime.today()).weekday() == 6):
            print('Its Sunday')
            date = datetime.today() - timedelta(days=2)
            date = str(date).split()[0]
            closing_time = f'{date} 15:59:00-05:00'
            return closing_time
        #check if today is saturday
        elif(datetime.date(datetime.today()).weekday() == 5):
            print('Its Saturday')
            date = datetime.today() - timedelta(days=1)
            date = str(date).split()[0]
            closing_time = f'{date} 15:59:00-05:00'
            del date
            return closing_time
        #if not saturday or sunday, but passed market closing, only pull data at closing time
        if(datetime.today().hour >= 15):
            print('Its after market close')
            date = datetime.today()
            date = str(date).split()[0]
            closing_time = f'{date} 15:59:00-05:00'
            return closing_time
        #if not passed market time, get hour and minute to pull proper data
        else:
            hour = datetime.today().hour
            minute = datetime.today().minute
            date = datetime.today()
            date = str(date).split()[0]
            if(minute >= 11):
                minute = minute - 1
                closing_time = f'{date} {hour+1}:{minute}:00-05:00'
            else:
                minute = minute - 1
                closing_time = f'{date} {hour+1}:0{minute}:00-05:00'
            return closing_time
    #if specific date is entered, then just pull closing data from that date
    else:
        closing_time = f'{date} 15:59:00-05:00'
    return closing_time
  
  
####################################################################
#PURPOSE: to compile a dataframe of all stocks in the chosen market
#ARGS: string
#RETURNS: pandas dataframe, pandas dataframe
#NOTE: this currently only has access to two groups of market (SP500 and NASDAQ)
#TO-DO: add functionality that allows access to different types of markets and tickers
####################################################################
def get_tickers(code):
    # First, create filter to remove NaN values to avoid them being calculated before trade day ends
    if code == 'NSDQ':
        my_tickers = si.tickers_nasdaq()
        spDataFrame= yf.download(tickers=my_tickers, interval='1m', period='5d')
        boolean = spDataFrame['Close']['AACG'] == spDataFrame['Close']['AACG']
    elif code == 'SPY':
        my_tickers = si.tickers_sp500()
        spDataFrame= yf.download(tickers=my_tickers, interval='1m', period='5d')
        boolean = spDataFrame['Close']['A'] == spDataFrame['Close']['A']
    else:
        return print('Acceptable Codes are: "NSDQ" for Nasdaq and "SPY" for S&P500')
    # Create dataframe with only volume
    volume = spDataFrame['Volume'][boolean]
    # Create dataframe with only closing price
    closing = spDataFrame['Close'][boolean]
    print(closing)
    return (volume, closing, my_tickers)

####################################################################
#PURPOSE: to return a list of filtered stocks that should give a minimum 1% return per day
#ARGS: pandas dataframe, pandas dataframe
#RETURNS: pandas dataframe
#NOTE: The list is still unstable due to lack of volatility analysis and lack of expert analysis reading
#TO-DO: add functionality that will auto-read expert analysis and will measure volatility (more volatile = better chance of upwards movement)
####################################################################
def get_recommendations(code):
    #get current date and time
    closing_time = get_date('2021-03-10')
    #get data based on stock market code
    volume, closing, my_tickers = get_tickers(code)
    recommendation_list={'Stock':[], 'Score':[], 'Volume':[], 'Closing Price':[], 'LowerBound':[], 'Volatility':[], 'Profit':[]}
    # This is a filtering for-loop
    for stock in my_tickers:
        # Filter by volume
        if(volume[stock][closing_time] >= 5000):
            lowerBound = closing[stock].rolling(window=25).mean() - 2*closing[stock].rolling(window=25).std()
            # Filter by standard deviation
            #TODO: Filter by volitility
            if(closing[stock][closing_time] < lowerBound[closing_time]):
                recommendation_list['Stock'].append(stock)
                
    # Fill in the recommendation List       
    for stock in recommendation_list['Stock']:
        #the upperbound of the standard deviation
        upperBound = closing[stock].rolling(window=25).mean() + 2*closing[stock].rolling(window=25).std()
        #the lowerbound of the standard deviation
        lowerBound = closing[stock].rolling(window=25).mean() - 2*closing[stock].rolling(window=25).std()
        #adding closing prices to recommendation list for clarity
        recommendation_list['Closing Price'].append(closing[stock][closing_time])
        #adding calculated Score to recommendation list for Clarity
        recommendation_list['Score'].append(((closing[stock][closing_time] - lowerBound[closing_time])/closing[stock][closing_time])*100)
        if(recommendation_list['Score'][-1] < 0):
            recommendation_list['Volatility'].append((upperBound[closing_time]-lowerBound[closing_time])/closing[stock][closing_time])
        else:
            recommendation_list['Volatility'].append(f'{(upperBound[closing_time]+lowerBound[closing_time])/2}::: stock shorting')
        recommendation_list['Profit'].append(((upperBound[closing_time]+lowerBound[closing_time])/2) - closing[stock][closing_time])
        recommendation_list['LowerBound'].append(lowerBound[closing_time])
        recommendation_list['Volume'].append(volume[stock][closing_time])
    recommendation_list = pd.DataFrame(recommendation_list)
    return recommendation_list
