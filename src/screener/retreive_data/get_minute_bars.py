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
from config import POLYGON_AGGS_MINUTE_URL, KEY
from .check_key import check_key
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
    #count = 0
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