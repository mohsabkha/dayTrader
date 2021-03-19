#BY: Mohammad Sabir Khan
####################################################################
#PURPOSE:
####################################################################
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import math
from datetime import datetime, timedelta, timezone
import time
import matplotlib.pyplot as plt
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
            closing_time = f'{date} 16:00:00-05:00'
            return closing_time, date
        #check if today is saturday
        elif(datetime.date(datetime.today()).weekday() == 5):
            print('Its Saturday')
            date = datetime.today() - timedelta(days=1)
            date = str(date).split()[0]
            closing_time = f'{date} 16:00:00-05:00'
            del date
            return closing_time, date
        #if not saturday or sunday, but passed market closing, only pull data at closing time
        if(datetime.today().hour >= 15):
            print('Its after market close')
            date = datetime.today()
            date = str(date).split()[0]
            closing_time = f'{date} 16:00:00-05:00'
            return closing_time, date
        #its before market open and its a monday
        elif(datetime.today().hour <= 3 and datetime.date(datetime.today()).weekday() == 0):
            print('Its before market opens and its Monday: Getting data from Friday')
            date = datetime.today() - timedelta(days=3)
            date = str(date).split()[0]
            closing_time = f'{date} 4:00:00-05:00'
            print(date)
            return closing_time, date
        #its before market open and its not monday
        elif(datetime.today().hour <= 3):
            print('Its before market opens')
            date = datetime.today() - timedelta(days=1)
            date = str(date).split()[0]
            closing_time = f'{date} 4:00:00-05:00'
            print(date)
            return closing_time, date
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
            return closing_time, date
    #if specific date is entered, then just pull closing data from that date
    else:
        closing_time = f'{date} 16:00:00-05:00'
    return closing_time, date

####################################################################
#PURPOSE: Set Endpoints For Polygon.io and certain constants
####################################################################
KEY = 'wN0pWKqQfTzBAfIOvCWf3v6iZBpr5otL'
POLYGON_URL = 'https://api.polygon.io'
POLYGON_TICKER_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'#page,key
POLYGON_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?unadjusted=true&apiKey={}'#ticker,start,end,key
POLYGON_DIV_URL = 'https://api.polygon.io/v2/reference/dividends/{}?apiKey={}'#ticker,key
POLYGON_SPLIT_URL = 'https://api.polygon.io/v2/reference/splits/{}?apiKey={}'#ticker,key
POLYGON_TYPES_URL = 'https://api.polygon.io/v2/reference/types?apiKey={}'#key
POLYGON_OPEN_CLOSE_URL = 'https://api.polygon.io/v1/open-close/{}/{}?unadjusted=true&apiKey={}'#ticker,date,key
POLYGON_AGGS_MINUTE_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}?unadjusted=true&sort=desc&limit=360&apiKey={}'#ticker,date,date,key
START = '2021-02-15'
CLOSING_TIME, END = get_date('2021-03-18')
TICKER_PAGE_PATH = '\\data\\tickers'

####################################################################
#PURPOSE: Get tickers from polygon.io
#ARGS: url
#RETURNS: n/a
#NOTE: this returns pages of tickers, not individual tickers
#TO-DO: n/a
####################################################################
def get_tickers(url=POLYGON_TICKER_URL):
    page = 1
    session = requests.Session()
    r = session.get(POLYGON_TICKER_URL.format(page, KEY))
    data = r.json()
    count = data['count']
    print('Polygon Returned {} Tickers'.format(count))
    print('Page {} Proccessed'.format(page))
    pages = math.ceil(count / data['perPage'])
    for page in range(2,pages+1):
        r = session.get(POLYGON_TICKER_URL.format(page, KEY))
        data = r.json()
        df = pd.DataFrame(data['tickers'])
        df.to_csv('data/tickers/{}.csv'.format(page), index=False)
        page += 1
        print("Page {} Proccessed".format(page))

####################################################################
#PURPOSE: extract individual tickers from pages
#ARGS: directory where pages of tickers are stored
#RETURNS: dataframe with tickers
#NOTE: n/a
#TO-DO: n/a
####################################################################
def combine_tickers(directory):
    df = pd.DataFrame()
    for f in os.listdir(directory):
        df2 = pd.read_csv("{}/{}".format(directory, f))
        df = df.append(df2)
    df.set_index('ticker', inplace=True)
    df.drop_duplicates()
    df.to_csv('polygon_tickers.csv')
    return df

####################################################################
#PURPOSE: Filter tickers for those that are tradable on most commision free platforms (webull, robinhood, etc.)
#ARGS: tickers dataframe
#RETURNS: list of ticker names
#NOTE:
#TO-DO:
####################################################################
def filter_us_stocks(ticker_df):
    df = ticker_df[(ticker_df.currency == 'USD') & (ticker_df.locale == 'US')]
    exch = ['ARCA', 'NASDAQ', 'NYE']
    df = df[df['primaryExch'].isin(exch)]
    stockTypes = ['PFD', 'ADR', 'CEF', 'MLP', 'RIGHT', 'UNIT', 'WRT']
    df = df[df['type'].isin(stockTypes) == False]
    df.to_csv('polygon_tickers_us.csv')
    symbols = df.index.tolist()
    return symbols

####################################################################
#PURPOSE: used to ensure that a key in a dictionary exists
#ARGS: dictionary, key
#RETURNS: the dictionary key value
#NOTE: n/a
#TO-DO: n/a
####################################################################
def check_key(dict, key): 
    if key in dict: 
        return dict[key]
    else: 
        return 'NaN'
    
####################################################################
#PURPOSE: get the opening and closing data for a specific date
#ARGS: list of symbols, polygon.io url endpoint
#RETURNS: list of data for each ticker
#NOTE:
#TO-DO:
####################################################################    
def get_open_close(symbols, url=POLYGON_OPEN_CLOSE_URL):
    print(':::::::::::::::::::GETTING DAILY OPEN AND CLOSE VALUES FOR ', END)
    session = requests.Session()
    # In case I run into issues, retry my connection
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    filter_data = {'symbol':[], 'volume':[], 'close':[], 'afterHours':[]}
    for symbol in symbols:
        try:
            r = session.get(url.format(symbol, END, KEY))
            if r:
                data = r.json()
                # create a pandas dataframe from the information
                if data['status'] == "OK":
                    filter_data['symbol'].append(symbol)
                    filter_data['volume'].append(data['volume'])
                    filter_data['close'].append(data['close'])
                    filter_data['afterHours'].append(data['afterHours'])
                else:
                    msg = ('No data for symbol ' + str(symbol))
                    print(msg)
            else:
                msg = ('No response for symbol ' + str(symbol))
                print(msg)
        # Raise exception but continue           
        except:
            msg = ('****** exception raised for symbol ' + str(symbol))
            print(msg)
    return filter_data

####################################################################
#PURPOSE: to filter out the useless stocks using volume traded and price
#ARGS: list of data containing ticker symbols
#RETURNS: filtered list of data
#NOTE: n/a
#TO-DO: n/a
####################################################################
#filter by price and volume
def first_data_filter(data):
    print(':::::::::::::::::::FILTERING DATA BASED ON PRICE AND VOLUME')
    first_filter = []
    for x in range(len(data['symbol'])):
        if((data['close'][x] >= 5) and (data['close'][x] <= 100) and (data['volume'][x] >= 500000)):
            first_filter.append(data['symbol'][x])
    return first_filter

####################################################################
#PURPOSE:
#ARGS:
#RETURNS:
#NOTE:
#TO-DO:
####################################################################
def get_minute_bars(first_filter, date, url=POLYGON_AGGS_MINUTE_URL):
    print(':::::::::::::::::::GETTING MINUTE BY MINUTE DATA FROM ', date)
    session = requests.Session()
    # In case I run into issues, retry my connection
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    count = 0
    my_list = {
            'symbol':[],
            'date':[],
            'open':[], 
            'close':[], 
            'high':[], 
            'low':[], 
            'volume':[],
            'weighted volume':[]
    }
    for symbol in first_filter:
        try:
            r = session.get(POLYGON_AGGS_MINUTE_URL.format(symbol, date, date, KEY))
            if r:
                data = r.json()
                # create a pandas dataframe from the information
                if data['queryCount'] > 1:
                    for result in data['results']:
                        my_list['symbol'].append(check_key(data, 'ticker'))
                        my_list['open'].append(check_key(result,'o'))
                        my_list['close'].append(check_key(result,'c'))
                        my_list['high'].append(check_key(result,'h'))
                        my_list['low'].append(check_key(result,'l'))
                        my_list['volume'].append(check_key(result,'v'))
                        my_list['weighted volume'].append(check_key(result,'vw'))
                        my_time = result['t']/1000.0
                        my_date = datetime.utcfromtimestamp(my_time).replace(tzinfo=timezone.utc)
                        my_list['date'].append(my_date)
                #if api did not contain any data
                else:
                    msg = ('No data for symbol ' + str(symbol))
                    print(msg)
            #if data was not returned from api
            else:
                msg = ('No response for symbol ' + str(symbol))
                print(msg)
            #after all dates are run, drop useless rows
        # Raise exception but continue           
        except:
            msg = ('****** exception raised for symbol ' + str(symbol))
            print(msg)
    return my_list

####################################################################
#PURPOSE:
#ARGS:
#RETURNS:
#NOTE:
#TO-DO:
####################################################################
def second_data_filter(filtered_symbols, minute_data, data):
    print(':::::::::::::::::::FILTERING DATA BASED ON PRICE CHANGE AND LOWERBOUND VOLATILITY')
    recommendation_list={
        'Stock':[], 
        'Score':[], 
        'Volume':[], 
        'Closing Price':[], 
        'LowerBound':[]
    }
    # This is a filtering for-loop
    for ticker in filtered_symbols:
        # This is the check on how active aftermarket the stock was
        percent_gained_after_market = (data['afterHours'][ticker] - data['close'][ticker])/data['afterHours'][ticker]
        if((percent_gained_after_market*100) > 2.0):
            #set up lower bollinger band for long buys
            closing = minute_data[minute_data['symbol'] == ticker]
            #closing.set_index('date', inplace=True)
            lowerBound = closing['close'].rolling(window=26).mean() - 2*closing['close'].rolling(window=26).std()
            #check if the afterhours close went below bollinger band
            lowerBound = pd.DataFrame(lowerBound)
            if(len(lowerBound.index) < 1):
                print(f'lowerbound was not found for {ticker}')
            elif(data['close'][ticker] < lowerBound['close'].iloc[-1]):
                the_close = data['close'][ticker]
                the_lower = lowerBound['close'].iloc[-1]
                print(f'added {ticker} with closing at {the_close} and lower bound at {the_lower}', ticker)
                #if it did, then the stock has high activity post market and it has decreased post
                recommendation_list['Stock'].append(ticker)
                recommendation_list['LowerBound'].append(lowerBound['close'].iloc[-1])
                recommendation_list['Closing Price'].append(data['close'][ticker])
                recommendation_list['Score'].append(((data['close'][ticker] - lowerBound['close'].iloc[-1])/data['close'][ticker])*100)
                recommendation_list['Volume'].append(data['volume'][ticker])
    return recommendation_list

####################################################################
#PURPOSE:
#ARGS:
#RETURNS:
#NOTE:
#TO-DO:
####################################################################
def get_daily_bars(symbols, start, end):
    print(f':::::::::::::::::::GETTING DAILY DATA FOR {start} through {end}')
    session = requests.Session()
    # In case I run into issues, retry my connection
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    count = 0
    my_list = {
            'symbol':[],
            'date':[],
            'close':[], 
            'volume':[],
            'weighted volume':[]
    }
    for symbol in symbols:
        try:
            r = session.get(POLYGON_AGGS_URL.format(symbol, start, end, KEY))
            if r:
                data = r.json()
                # create a pandas dataframe from the information
                if data['queryCount'] > 1:
                    print('::: added stock :::')
                    for result in data['results']:
                        my_list['symbol'].append(check_key(data, 'ticker'))
                        my_list['close'].append(check_key(result,'c'))
                        my_list['volume'].append(check_key(result,'v'))
                        my_list['weighted volume'].append(check_key(result,'vw'))
                        my_time = result['t']/1000.0
                        my_date = datetime.utcfromtimestamp(my_time).replace(tzinfo=timezone.utc)
                        my_list['date'].append(my_date)
                #if api did not contain any data
                else:
                    msg = ('No data for symbol ' + str(symbol))
                    print(msg)
            #if data was not returned from api
            else:
                msg = ('No response for symbol ' + str(symbol))
                print(msg)
            #after all dates are run, drop useless rows
        # Raise exception but continue           
        except:
            msg = ('****** exception raised for symbol ' + str(symbol))
            print(msg)
    return my_list

####################################################################
#PURPOSE:
#ARGS:
#RETURNS:
#NOTE:
#TO-DO:
####################################################################
def send_email():
    print('hi')
