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
from config import POLYGON_OPEN_CLOSE_URL, END, KEY

    
####################################################################
#PURPOSE: get the opening and closing data for a specific date
#ARGS: list of symbols, polygon.io url endpoint
#RETURNS: list of data for each ticker
#NOTE:
#TO-DO:
####################################################################    
def get_open_close(symbols, url=POLYGON_OPEN_CLOSE_URL):
    print(':::::::::::::::::::ENTERED GET OPEN CLOSE FOR', END)
    session = requests.Session()
    # In case I run into issues, retry my connection
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    filter_data = {'symbol':[], 'volume':[], 'close':[], 'afterHours':[]}
    loading_counter = 0
    loading_animations = ['|', '/', '-', '\\']
    for symbol in symbols:
        try:
            msg = ' loading open/close data: ' + loading_animations[loading_counter]
            print(msg, end='\r')
            if(loading_counter==3):
                loading_counter = 0
            else:
                loading_counter = loading_counter+1
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
            else:
                msg = ('No response for symbol ' + str(symbol))
        # Raise exception but continue           
        except:
            msg = ('****** exception raised for symbol ' + str(symbol))
            print(msg)
    print('loading open/close data: FINISHED LOADED OPEN/CLOSE DATA')
    return filter_data