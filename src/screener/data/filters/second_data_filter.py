import pandas as pd

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