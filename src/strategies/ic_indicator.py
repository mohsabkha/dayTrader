import pandas as pd

def ic_indicator(ticker_values, ic_data):
    print(':::::::::::::::::::ENTERING IC INDICATOR')
    ticker_series_high = pd.Series(ticker_values['high'])
    ticker_series_low = pd.Series(ticker_values['low'])
    try:
        #conversion line takes 9 period high + 9 period low / 2
        ic_data['conversion_line'].append((ticker_series_high.rolling(window=9).max() + 
                                        ticker_series_low.rolling(window=9).min())/2)
        print(':::::::::::::::::::IC INDICATOR - created conversion line')
    except:
        print('error log START: on IC conversion line------------------------------------------')
        print('DATA: ticker values: ',ticker_values)
        print('DATA: ticker values high type: ', type(ticker_series_high))
        print('DATA: ticker values high: ', ticker_series_high)
        print('DATA: ticker values 9 period high: ', ticker_series_high.rolling(window=9))
        print('DATA: ticker values 9 period high max: ', ticker_series_high.rolling(window=9).max())
        print('DATA: ticker values 9 period low min: ', ticker_series_low.rolling(window=9).min()) 
        print('error log END: on IC conversion line------------------------------------------')
    try:
        #base line takes 26 period high + 26 period low / 2
        ic_data['base_line'].append((ticker_series_high.rolling(window=26).max() + 
                                    ticker_series_low.rolling(window=26).min())/2)
        print(':::::::::::::::::::IC INDICATOR - created base line')
    except:
        print('error log START: on IC base line------------------------------------------')
        print('DATA: ticker values 26 period high max: ', ticker_series_high.rolling(window=26).max())
        print('DATA: ticker values 26 period low min: ', ticker_series_low.rolling(window=26).min())
        print('error log END: on IC base line------------------------------------------')


    try:
        #lead span is coversion line + base line / 2 and shifted 26 periods into the future
        ic_data['lead_A'].append((ic_data['conversion_line'][-1] + ic_data['base_line'][-1])/2)
        print(':::::::::::::::::::IC INDICATOR - created lead A')
    except:
        print('error log START: on IC lead A------------------------------------------')
        print('DATA: conversion line type: ', type(ic_data['conversion_line'][-1]))
        print('DATA: conversion line: ', ic_data['conversion_line'][-1])
        print('DATA: base line type: ', ic_data['base_line'][-1])
        print('DATA: base line: ', ic_data['base_line'][-1])
        print('error log END: on IC lead A------------------------------------------')
    try:
        #lead span b is the 52 period high + the 52 period low / 2
        ic_data['lead_B'].append((ticker_series_high.rolling(window=52).max() + 
                                ticker_series_low.rolling(window=52).min())/2)
        print(':::::::::::::::::::IC INDICATOR - created lead B')
    except:
        print('error log START: on IC lead B------------------------------------------')
        print('DATA: ticker values 52 period high max: ', ticker_series_high.rolling(window=52).max())
        print('DATA: ticker values 52 period low min: ', ticker_series_low.rolling(window=52).min())
        print('error log END: on IC lead B------------------------------------------')
    try:
        #the lagging span is 26 periods in the past
        ic_data['lag_span'].append(ticker_values['close'][-1])
        print(':::::::::::::::::::IC INDICATOR - created lagging span')
    except:
        print('error log START: on IC lagging span------------------------------------------')
        print('DATA: ticker values close last index: ', ticker_values['close'][-1])
        print('error log END: on IC lagging span------------------------------------------')
        #series of checks
    
    if(len(ic_data['lead_A']) > 53):
        #conversion line is greater than base line in the present
        flag1 = ic_data['coversion_line'][-1] > ic_data['base_line'][-1]
        if flag1: print('conversion line was greater than base line')
        #lagging span in greater than the cloud (the cloud is both leads) in the past
        flag2 = ic_data['lag_span'][-1] > ic_data['lead_A'][-52]
        flag3 = ic_data['lag_span'][-1] > ic_data['lead_B'][-52]
        if flag2 and flag3: print('lagging span was above the cloud')
        #current ticker values close higher than the cloud in the present but open below the cloud
        flag4 = ticker_values['close'][-1] > ic_data['lead_A'][-26]
        flag5 = ticker_values['close'][-1] > ic_data['lead_B'][-26]
        flag6 = ticker_values['open'][-1] < ic_data['lead_B'][-26] or ticker_values['open'][-1] < ic_data['lead_A'][-26]
        if flag4 and flag5 and flag6: print('price opened in or below the cloud but closed above')
        #the cloud is green in the future
        flag7 = ic_data['lead_A'][-1] > ic_data['lead_B'][-1]
        if flag2: print('the cloud is green')
        #check if all conditions are true in order to buy
        print(':::::::::::::::::::CHECKING IC FLAGS')
        if(flag1 and flag2 and flag3 and flag4 and flag5 and flag6 and flag7):
            # TO-DO : set profit loss/gain here and return it
            print(':::::::::::::::::::IC INDICATOR RETURNED TRUE')
            return True
        else:
            return False
    else:
        return False

