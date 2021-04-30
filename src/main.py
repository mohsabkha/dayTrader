# make sure you create this file based on config_example.py
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
from apscheduler.schedulers.blocking import BlockingScheduler

import pandas as pd
import numpy as np
from datetime import datetime
import time
from polygon import WebSocketClient, STOCKS_CLUSTER
import os


def main(jobType):
    # Phase 1 - get tickers
    try:
        # get the current time
        now = datetime.now().strftime('%H:%M:%S')
        print(':::::::::::::::::::START TIME IS', now)
        # check current directory
        dir_path = os.getcwd()
        tickerPagePath = os.path.join(dir_path, "polygon_data", "tickers")
        dir = os.listdir(tickerPagePath)
        # if the path does not have ticker files, get ticker files
        if(len(dir) == 0):
            get_tickers()
        # use combine tickers to ensure all ticker data from get_tickers is correct
        datetime.now().strftime('%H:%M:%S')
        print(':::::::::::::::::::ENTERING COMBINE TICKERS -',
              datetime.now().strftime('%H:%M:%S'))
        # store ticker data into symbols
        symbols = combine_tickers('polygon_data/tickers')
        # combine tickers will create csv files, read those csv files into polygon_tickers with
        # symbols variable as backup
        polygon_tickers = pd.read_csv('polygon_tickers.csv')
        # set dataframe index as the ticker
        polygon_tickers.set_index('ticker', inplace=True)
        # remove duplicates of the tickers
        polygon_tickers.drop_duplicates()
        # filter out tickers that are not bought and sold on common us exchanges and reassign them to
        # symbols variable
        print(':::::::::::::::::::ENTERING FILTER US STOCKS',
              datetime.now().strftime('%H:%M:%S'))
        symbols = filter_us_stocks(polygon_tickers)
    except Exception as e:
        print('error log: Error In Phase 1 ------------------------------------------')
        print(e)

    # Phase 2 - get data
    try:
        # returns end of day data for symbols
        print(':::::::::::::::::::ENTERING GET OPEN CLOSE',
              datetime.now().strftime('%H:%M:%S'))
        data = get_open_close(symbols)
        # returns a list of symbols that met criteria for day trades
        print(':::::::::::::::::::DATA BEING SENT TO FIRST DATA FILTER',
              datetime.now().strftime('%H:%M:%S'))
        print(':::::::::::::::::::This is the length of that data: ', len(data))
        print(':::::::::::::::::::ENTERING FIRST DATA FILTER -',
              datetime.now().strftime('%H:%M:%S'))
        filtered_data = first_data_filter(data)
        # retrieves minute data for symbols that met criteria
        print(':::::::::::::::::::ENTERING GET MINUTE BARS -',
              datetime.now().strftime('%H:%M:%S'))
        minute_data = get_minute_bars(first_filter=filtered_data, date=END)
        almost_clean_data = pd.DataFrame(minute_data)
        almost_clean_data = almost_clean_data.reindex(
            index=almost_clean_data.index[::-1])
        # use daily open close rates for each ticker and convert it to dataframe
        daily_data = pd.DataFrame(data)
        daily_data.set_index('symbol', inplace=True)
        # filter remaining data again
        print(':::::::::::::::::::ENTERING SECOND DATA FILTER -',
              datetime.now().strftime('%H:%M:%S'))
        recommendation_list = second_data_filter(
            filtered_data, almost_clean_data, daily_data)
        recommendation_list = pd.DataFrame(recommendation_list)
        # print date to ensure that correct date is being used
        print(':::::::::::::::::::The following data is being taken from this date: ', END)
    except Exception as e:
        print('error log: Error In Phase 2 ------------------------------------------')
        print(e)

    # Phase 3 - organize filtered data and conduct initial buys
    # sort data by certain values
    try:
        my_volume_list_best = recommendation_list.sort_values(
            by='Volume').tail(5)
        my_score_list = recommendation_list.sort_values(by='Score').head(5)
        # print time to see how long it took to complete process
        now = datetime.now().strftime('%H:%M:%S')
        print(':::::::::::::::::::END TIME IS ', now)
        # remove combined tickers data
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
        del tickerPagePath
        del now
        print('\n\n\n:::::::::::::::::::Top Stocks Based On Score')
        print(my_score_list)
        my_score_list.to_csv('top_five_stocks.csv')
        print('\n\n\n:::::::::::::::::::Top Stocks Based On Highest Volume')
        print(my_volume_list_best)
        print('\n\n\n:::::::::::::::::::CONDTIONING DATA FOR ALPACA')
        # format data for alpaca that will be called in the next phase
        alpaca_top_stocks_array = condition_data(my_score_list)
        # buy all stocks
        if (jobType == '4am'):
            print(':::::::::::::::::::BUYING STOCKS FOR EXPERIMENT 1')
            ps_gonzalo = PurchaseStock(
                APCA_API_KEY_ID_GONZALO,
                APCA_API_SECRET_KEY_GONZALO,
                APCA_API_BASE_URL_PAPER_GONZALO,
                alpaca_top_stocks_array,
                BUY_LIMIT_GONZALO)
            ps_gonzalo.run()
        # buy one stock
        if (jobType == '7am'):
            print(':::::::::::::::::::BUYING STOCKS FOR EXPERIMENT 2')
            to_list = [alpaca_top_stocks_array[0]]
            ps_sam = PurchaseStock(
                APCA_API_KEY_ID_MO,
                APCA_API_SECRET_KEY_MO,
                APCA_API_BASE_URL_PAPER_MO,
                to_list,
                BUY_LIMIT_SAM)
            ps_sam.run()
    except Exception as e:
        print('error log: Error In Phase 3 ------------------------------------------')
        print(e)
    # Phase 4 - get live data and feed into strat for experiments 3-5
    try:
        if (jobType == '831am'):
            print(':::::::::::::::::::CONDTIONING DATA FOR WEBSOCKET')
            stock_score = my_score_list.set_index('Stock')
            websocket_symbols, websocket_ticker_data, ic_data = strat_list(
                stock_score)
            # function to be used by websocket

            def entry_to_strats(message):
                strats(message, websocket_ticker_data, ic_data)
            # begin opening websocket
            print(':::::::::::::::::::OPENING WEBSOCKET')
            my_client = WebSocketClient(STOCKS_CLUSTER, KEY, entry_to_strats)
            # run it asyncronously
            my_client.run_async()
            # subscribe to all stocks in the list
            print(':::::::::::::::::::SUBSCRIBING TO STOCKS IN WEBSOCKET')
            for ticker in websocket_symbols:
                my_client.subscribe(ticker)
                # busy waiting loop that prevents the socket from closing
            print(':::::::::::::::::::ENTERING BUSY WAITING WHILE DATA IS COLLECTED')
            timer = True
            while(timer):
                # if 6 < hour < 12
                if(datetime.now().hour > 10 and datetime.now() < 12):
                    print(':::::::::::::::::::CLOSING WEBSOCKET')
                    my_client.close_connection()
                    timier = False
    except Exception as e:
        print('error log: Error In Phase 4 ------------------------------------------')
        print(e)


# if __name__ == "__main__":
#     # to run this using python main.py, remember to use this commaned in terminal before running: export PYTHONPATH="$PWD/src"
#     main()


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9, )
def fourAm():
    print('It is 4 am CST, I will buy for Gonzalo')
    main('4am')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12)
def sevenAm():
    print('It is 7 am CST, I will buy for Mo')
    main('7am')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=13, minute=31)
def eightThirtyOneAm():
    print('It is 8:31 am CST, I will buy for Mo')
    main('831am')

# TODO: Have alpacha sell all stocks at 8:55 am
# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=8, minute=55)
# def sellAllStocks():
#     print("It is 8:55 am, I'll tell alpaca to sell all stocks if it hasn't hit it's price target")
#     main('831am')


sched.start()
