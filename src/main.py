#make sure you create this file based on config_example.py
from config import *

from screener.retreive_data.ticker_functions.get_tickers import get_tickers
from screener.retreive_data.ticker_functions.combine_tickers import combine_tickers
from screener.retreive_data.get_open_close import get_open_close
from screener.retreive_data.get_minute_bars import get_minute_bars
from screener.retreive_data.get_daily_bars import get_daily_bars
from screener.filters.filter_us_stocks import filter_us_stocks
from screener.filters.first_data_filter import first_data_filter
from screener.filters.second_data_filter import second_data_filter
from alpaca.condition_data import condition_data
from strategies.strats import strats
from strategies.strat_list import strat_list
from alpaca.trade import PurchaseStock

import pandas as pd
import numpy as np
from datetime import datetime
import time
from polygon import WebSocketClient, STOCKS_CLUSTER
import os

def main():
    ######################################################### Phase 1 - get tickers
    #get the current time
    now = datetime.now().strftime('%H:%M:%S')
    print(':::::::::::::::::::START TIME IS', now)
    #check current directory
    dir_path = os.getcwd()
    path = (dir_path + TICKER_PAGE_PATH)
    dir = os.listdir(path)
    #if the path does not have ticker files, get ticker files
    if(len(dir) == 0):
        get_tickers()
    #use combine tickers to ensure all ticker data from get_tickers is correct    
    datetime.now().strftime('%H:%M:%S')
    print(':::::::::::::::::::ENTERING COMBINE TICKERS -',datetime.now().strftime('%H:%M:%S'))
    #store ticker data into symbols
    symbols = combine_tickers('polygon_data/tickers')
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
    print(':::::::::::::::::::This is the length of that data: ',len(data))
    print(':::::::::::::::::::ENTERING FIRST DATA FILTER -',datetime.now().strftime('%H:%M:%S'))
    filtered_data = first_data_filter(data)
    #retrieves minute data for symbols that met criteria
    print(':::::::::::::::::::ENTERING GET MINUTE BARS -',datetime.now().strftime('%H:%M:%S'))
    minute_data = get_minute_bars(first_filter=filtered_data, date=END)
    almost_clean_data = pd.DataFrame(minute_data)
    almost_clean_data = almost_clean_data.reindex(index=almost_clean_data.index[::-1])
    #use daily open close rates for each ticker and convert it to dataframe
    daily_data = pd.DataFrame(data)
    daily_data.set_index('symbol', inplace=True)
    #filter remaining data again
    print(':::::::::::::::::::ENTERING SECOND DATA FILTER -', datetime.now().strftime('%H:%M:%S'))
    recommendation_list = second_data_filter(filtered_data, almost_clean_data, daily_data)
    recommendation_list = pd.DataFrame(recommendation_list)
    #print date to ensure that correct date is being used
    print(':::::::::::::::::::The following data is being taken from this date: ', END)


    ######################################################### Phase 3 - organize filtered data
    #sort data by certain values
    my_volume_list_best = recommendation_list.sort_values(by='Volume').tail(5)
    my_score_list = recommendation_list.sort_values(by='Score').head(5)
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
    print('\n\n\n:::::::::::::::::::Top Stocks Based On Score')
    print(my_score_list)
    my_score_list.to_csv('top_five_stocks.csv')
    print('\n\n\n:::::::::::::::::::Top Stocks Based On Highest Volume')
    print(my_volume_list_best)
    print('\n\n\n:::::::::::::::::::CONDTIONING DATA FOR ALPACA')
    #format data for alpaca that will be called in the next phase
    alpaca_top_stocks_frame, alpaca_top_stocks_array = condition_data(my_score_list)


    ######################################################### Phase 4 - get live data and feed into strat for experiments 3-5
    print(':::::::::::::::::::CONDTIONING DATA FOR WEBSOCKET')
    stock_score = my_score_list.set_index('Stock')
    # websocket client calls strats(); 
        # strats() calls ic_strat() and vwap_strat; 
            # ic_strat() and vwap_strat return true or false; 
        # strats() then calls alpaca if conditions are true
    websocket_symbols, websocket_ticker_data, ic_data = strat_list(stock_score)
    #function to be used by websocket
    def entry_to_strats(message):
        strats(message, websocket_ticker_data, ic_data)
    #begin opening websocket
    print(':::::::::::::::::::OPENING WEBSOCKET')
    my_client = WebSocketClient(STOCKS_CLUSTER, KEY, entry_to_strats)
    #run it asyncronously
    my_client.run_async()
    #subscribe to all stocks in the list
    print(':::::::::::::::::::SUBSCRIBING TO STOCKS IN WEBSOCKET')
    for ticker in websocket_symbols:
        my_client.subscribe(ticker)
    #busy waiting loop that prevents the socket from closing
    print(':::::::::::::::::::ENTERING BUSY WAITING WHILE DATA IS COLLECTED')
    timer = True
    while( timer ):
        #if its 8:31, then close the loop
        if(datetime.now().hour >= 8 and datetime.now().minute < 30):
            timer = False
    #buy all stocks
    print(':::::::::::::::::::BUYING STOCKS FOR EXPERIMENT 1')
    ps_gonzalo = PurchaseStock(
        APCA_API_KEY_ID_GONZALO,
        APCA_API_SECRET_KEY_GONZALO, 
        APCA_API_BASE_URL_PAPER_GONZALO, 
        alpaca_top_stocks_array,
        BUY_LIMIT_GONZALO)
    #buy one stock
    print(':::::::::::::::::::BUYING STOCKS FOR EXPERIMENT 2')
    ps_sam = PurchaseStock(
        APCA_API_KEY_ID_SAM,
        APCA_API_SECRET_KEY_SAM,
        APCA_API_BASE_URL_PAPER_SAM, 
        alpaca_top_stocks_array[0], 
        BUY_LIMIT_SAM)
    print(':::::::::::::::::::CALL TO SLEEP, PREVENT WEBSOCKET CLOSING')
    time.sleep(16000)
    #sell off
    print(':::::::::::::::::::CLOSING WEBSOCKET')
    my_client.close_connection()
if __name__ == "__main__":
    #to run this using python main.py, remember to use this commaned in terminal before running: export PYTHONPATH="$PWD/src"
    main()
    