#get date and ensure that it is correct
now = datetime.now().strftime('%H:%M:%S')
print(':::::::::::::::::::START TIME IS ', now)

#get current directoy and ensure pages of tickers are stored in them
dir_path = os.getcwd()
path = (dir_path + TICKER_PAGE_PATH)
dir = os.listdir(path) 
if(len(dir) == 0):
    get_tickers()
#time check to see how long get_tickers() took to complete
datetime.now().strftime('%H:%M:%S')

#launching combine tickers
print(':::::::::::::::::::ENTERING COMBINE TICKERS - ',datetime.now().strftime('%H:%M:%S'))
symbols = combine_tickers('data/tickers')

#getting dataframe from csv file created with combine_tickers()
polygon_tickers = pd.read_csv('polygon_tickers.csv')
polygon_tickers.set_index('ticker', inplace=True)
polygon_tickers.drop_duplicates()

#filtering out non-US stocks
print(':::::::::::::::::::ENTERING FILTER US STOCKS',datetime.now().strftime('%H:%M:%S'))
symbols = filter_us_stocks(polygon_tickers)

#returns end of day data for symbols
print(':::::::::::::::::::ENTERING GET OPEN CLOSE',datetime.now().strftime('%H:%M:%S'))
data = get_open_close(symbols)
daily_data = pd.DataFrame(data)
daily_data.set_index('symbol', inplace=True)

#returns a list of symbols that met criteria for day trades and checking its data
print(':::::::::::::::::::DATA BEING SENT TO FIRST DATA FILTER',datetime.now().strftime('%H:%M:%S'))
print(':::::::::::::::::::This is the length of that data\n',len(data))

#first algorithmic filter
print(':::::::::::::::::::ENTERING FIRST DATA FILTER - ',datetime.now().strftime('%H:%M:%S'))
filtered_data = first_data_filter(data)

#retrieves minute data for symbols that met criteria
print(':::::::::::::::::::ENTERING GET MINUTE BARS - ',datetime.now().strftime('%H:%M:%S'))
minute_data = get_minute_bars(first_filter=filtered_data, date='2021-03-15')
almost_clean_data = pd.DataFrame(minute_data)

#reverse minute data
almost_clean_data = almost_clean_data.reindex(index=almost_clean_data.index[::-1])

#second algorithmic data filter
print(':::::::::::::::::::ENTERING SECOND DATA FILTER - ', datetime.now().strftime('%H:%M:%S'))
recommendation_list = second_data_filter(filtered_data, almost_clean_data, daily_data)
#turn it into a dataframe
recommendation_list = pd.DataFrame(recommendation_list)

#display data
print(':::::::::::::::::::The following data is being taken from this date: ', END);
recommendation_list.sort_values(by='Volume').tail(7)

#display the time when the program comes to an end
now = datetime.now().strftime('%H:%M:%S')
print(':::::::::::::::::::END TIME IS ', now)

#delete combine tickers file so fresh batch can be created next run
os.remove("polygon_tickers_us.csv")
