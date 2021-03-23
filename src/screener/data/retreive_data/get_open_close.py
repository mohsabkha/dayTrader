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
from .screener_config import POLYGON_OPEN_CLOSE_URL, END, KEY

    
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