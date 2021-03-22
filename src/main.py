from screener.data.retreiveData.screener_config import TICKER_PAGE_PATH, END
from screener.data.retreiveData.tickers.get_tickers import get_tickers
from screener.data.retreiveData.tickers.combine_tickers import combine_tickers
from screener.data.retreiveData.get_open_close import get_open_close
from screener.data.retreiveData.get_minute_bars import get_minute_bars
from screener.data.retreiveData.get_daily_bars import get_daily_bars
from screener.data.filters.filter_us_stocks import filter_us_stocks
from screener.data.filters.first_data_filter import first_data_filter
from screener.data.filters.second_data_filter import second_data_filter

import pandas as pd
import numpy as np
from datetime import datetime
import os

def main():
    ######################################################### Phase 1 - get tickers
    #get current time
    now = datetime.now().strftime('%H:%M:%S')
    print(':::::::::::::::::::START TIME IS ', now)

    #check current directory
    dir_path = os.getcwd()
    path = (dir_path + TICKER_PAGE_PATH)
    dir = os.listdir(path)

    #if the path does not have ticker files, get ticker files
    if(len(dir) == 0):
        get_tickers()

    #use combine tickers to ensure all ticker data from get_tickers is correct    
    datetime.now().strftime('%H:%M:%S')
    print(':::::::::::::::::::ENTERING COMBINE TICKERS - ',datetime.now().strftime('%H:%M:%S'))

    #store ticker data into symbols
    symbols = combine_tickers('data/tickers')

    #combine tickers will create csv files, read those csv files into polygon_tickers with 
    #symbols variable as backup
    polygon_tickers = pd.read_csv('polygon_tickers.csv')

    #set dataframe index as the ticker
    polygon_tickers.set_index('ticker', inplace=True)

    #remove duplicates of the tickers
    polygon_tickers.drop_duplicates()

    #filter out tickers that are not bought and sold on common us exchanges and reassign them to 
    #symbols variable
    print(':::::::::::::::::::ENTERING FILTER US STOCKS',datetime.now().strftime('%H:%M:%S'))
    symbols = filter_us_stocks(polygon_tickers)




    ######################################################### Phase 2 - get data
    #returns end of day data for symbols
    print(':::::::::::::::::::ENTERING GET OPEN CLOSE',datetime.now().strftime('%H:%M:%S'))
    data = get_open_close(symbols)

    #returns a list of symbols that met criteria for day trades
    print(':::::::::::::::::::DATA BEING SENT TO FIRST DATA FILTER',datetime.now().strftime('%H:%M:%S'))
    print(':::::::::::::::::::This is the length of that data\n',len(data))
    print(':::::::::::::::::::ENTERING FIRST DATA FILTER - ',datetime.now().strftime('%H:%M:%S'))
    filtered_data = first_data_filter(data)

    #retrieves minute data for symbols that met criteria
    print(':::::::::::::::::::ENTERING GET MINUTE BARS - ',datetime.now().strftime('%H:%M:%S'))
    minute_data = get_minute_bars(first_filter=filtered_data, date='2021-03-15')
    almost_clean_data = pd.DataFrame(minute_data)
    almost_clean_data = almost_clean_data.reindex(index=almost_clean_data.index[::-1])

    #use daily open close rates for each ticker and convert it to dataframe
    daily_data = pd.DataFrame(data)
    daily_data.set_index('symbol', inplace=True)

    #filter remaining data again
    print(':::::::::::::::::::ENTERING SECOND DATA FILTER - ', datetime.now().strftime('%H:%M:%S'))
    recommendation_list = second_data_filter(filtered_data, almost_clean_data, daily_data)
    recommendation_list = pd.DataFrame(recommendation_list)

    #print date to ensure that correct date is being used
    print(':::::::::::::::::::The following data is being taken from this date: ', END)




    ######################################################### Phase 3 - organize filtered data
    #sort data by certain values
    my_volume_list_best = recommendation_list.sort_values(by='Volume').tail(10)
    my_volume_list_worst = recommendation_list.sort_values(by='Volume').head(10)
    my_score_list = recommendation_list.sort_values(by='Score').head(10)

    #print time to see how long it took to complete process
    now = datetime.now().strftime('%H:%M:%S')
    print(':::::::::::::::::::END TIME IS ', now)

    #remove combined tickers data
    os.remove("polygon_tickers_us.csv")
    del symbols
    del polygon_tickers
    del data
    del filtered_data
    del minute_data
    del almost_clean_data
    del daily_data
    del recommendation_list
    del dir_path
    del path
    del now

    print(my_score_list)
    print(my_volume_list_best)
    print(my_volume_list_worst)

    ######################################################### Phase 4 - get live data and feed into strat
    #loop/websocket for live feed    
        #ic_indicator_strat(data)
            #feed live data into the function and get analysis on when you should buy
        #vwap_indicator_strat(data)
            #feed live data into the function and get analysis on when you should buy
        #if vwap and ic are both true, trigger alpaca 
        #to buy the stock at that time with take profit and stop loss built in
        #break out of loop / end socket connection
        #run_connection()
    
    