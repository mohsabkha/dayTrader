#make sure you create this file based on sample_screener_config.py
from ......config import POLYGON_TICKER_URL, KEY
import requests
import math
import pandas as pd
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