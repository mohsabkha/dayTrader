def ic_indicator(ticker_values, ic_data):
    #conversion line takes 9 period high + 9 period low / 2
    ic_data['conversion_line'].append((ticker_values['high'].rolling(window=9).max() + 
                                       ticker_values['low'].rolling(window=9).min())/2)
    
    #base line takes 26 period high + 26 period low / 2
    ic_data['base_line'].append((ticker_values['high'].rolling(window=26).max() + 
                                 ticker_values['low'].rolling(window=26).min())/2)
    
    #lead span is coversion line + base line / 2 and shifted 26 periods into the future
    ic_data['lead_A'].append((conversion_line + base_line)/2)
    
    #lead span b is the 52 period high + the 52 period low / 2
    ic_data['lead_B'].append((ticker_values['high'].rolling(window=52).max() + 
                              ticker_values['low'].rolling(window=52).min())/2)
    
    #the lagging span is the 
    ic_data['lag_span'].append(ticker_values['close'][-26])
    
    #series of checks
    if(len(ic_data['lead_A']) > 53):
        flag1 = ic_data['coversion_line'][-1] > ic_data['base_line'][-1]
        flag2 = ic_data['lag_span'][-1] > ic_data['lead_A'][-52]
        flag3 = ic_data['lag_span'][-1] > ic_data['lead_B'][-52]
        flag4 = ticker_values['close'] > ic_data['lead_A'][-26]
        flag5 = ticker_values['close'] > ic_data['lead_B'][-26]
        flag6 = ic_data['lead_A'][-1] > ic_data['lead_B'][-1]
        if(flag1 and flag2 and flag3 and flag4 and flag5 and flag6):
            return True
        else:
            return False
    else: 
        return False