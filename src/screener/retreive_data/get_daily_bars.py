
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
#make sure you create this file based on sample_screener_config.py
from config import POLYGON_AGGS_URL, KEY
from .check_key import check_key

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
    #count = 0
    my_list = {
            'symbol':[],
            'date':[],
            'close':[], 
            'volume':[],
            'weighted volume':[]
    }
    loading_counter = 0
    loading_animations = ['|', '/', '-', '\\']
    for symbol in symbols:
        try:
            msg = ' loading daily data: ' + loading_animations[loading_counter]
            print(msg, end='\r')
            if(loading_counter==3):
                loading_counter = 0
            else:
                loading_counter = loading_counter+1
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
            #if data was not returned from api
            else:
                msg = ('No response for symbol ' + str(symbol))
            #after all dates are run, drop useless rows
        # Raise exception but continue           
        except:
            msg = ('****** exception raised for symbol ' + str(symbol))
            print(msg)
    print('loading daily data: FINISHED LOADED DAILY DATA')
    return my_list