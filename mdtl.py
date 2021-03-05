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
def get_date():
    #set up start and end dates of query (end day will be today, start day will be yesterday)
    last_day_of_the_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    today = datetime.today()
    
    day=today.day
    month=today.month
    year=today.year
    date = str(today).split()[0]
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
        spDataFrame= yf.download(tickers=my_tickers, interval='1m', start='2021-02-24', end='2021-03-03')
        boolean = spDataFrame['Close']['A'] == spDataFrame['Close']['A']
    else:
        print('Acceptable Codes are: "NSDQ" for Nasdaq and "SPY" for S&P500')
    # Create dataframe with only volume
    volume = spDataFrame[boolean]['Volume']
    # Create dataframe with only closing price
    closing = spDataFrame[boolean]['Close']
    
    return (volume, closing)

####################################################################
#PURPOSE: to return a list of filtered stocks that should give a minimum 1% return per day
#ARGS: pandas dataframe, pandas dataframe
#RETURNS: pandas dataframe
#NOTE: The list is still unstable due to lack of volatility analysis and lack of expert analysis reading
#TO-DO: add functionality that will auto-read expert analysis and will measure volatility (more volatile = better chance of upwards movement)
####################################################################
def get_recommendations(volume, closing):
    closing_time = get_date()
    recommendation_list={'Stock':[], 'Score':[], 'Volume':[], 'Closing Price':[], 'LowerBound':[], 'PriceToSell':[], 'Profit':[]}
    # This is a filtering for-loop
    for stock in my_tickers:
        # Filter by volume
        if(volume[stock][closing_time] >= 300000):
            lowerBound = closing[stock].rolling(window=30).mean() - 2*closing[stock].rolling(window=30).std()
            # Filter by standard deviation
            #TODO: Filter by volitility
            if(closing[stock][closing_time] < lowerBound[closing_time]):
                print(f'{stock}\nThe lower Bound vs Closing Price: {lowerBound[closing_time]} vs {closing[stock][closing_time]}')
                recommendation_list['Stock'].append(stock)
    # Fill in the recommendation List       
    for stock in recommendation_list['Stock']:
        #the upperbound of the standard deviation
        upperBound = closing[stock].rolling(window=30).mean() + 2*closing[stock].rolling(window=30).std()
        #the lowerbound of the standard deviation
        lowerBound = closing[stock].rolling(window=30).mean() - 2*closing[stock].rolling(window=30).std()
        #adding closing prices to recommendation list for clarity
        recommendation_list['Closing Price'].append(closing[stock][closing_time])
        #adding calculated Score to recommendation list for Clarity
        recommendation_list['Score'].append(((closing[stock][closing_time] - lowerBound[closing_time])/closing[stock][closing_time])*100)
        if(recommendation_list['Score'][-1] < 0):
            recommendation_list['PriceToSell'].append((upperBound[closing_time]+lowerBound[closing_time])/2)
        else:
            recommendation_list['PriceToSell'].append(f'{(upperBound[closing_time]+lowerBound[closing_time])/2}::: stock shorting')
        recommendation_list['Profit'].append(((upperBound[closing_time]+lowerBound[closing_time])/2) - closing[stock][closing_time])
        recommendation_list['LowerBound'].append(lowerBound[closing_time])
        recommendation_list['Volume'].append(volume[stock][closing_time])
    recommendation_list = pd.DataFrame(recommendation_list)
    return recommendation_list
