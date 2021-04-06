def vwap_indicator(ticker_values):
    print(':::::::::::::::::::ENTERING VWAP INDICATOR')
    #if open is lower than vwap and close is higher
    if (ticker_values['open'][-1] < ticker_values['vwap'][-1]  and ticker_values['close'][-1] > ticker_values['vwap'][-1]):
        return True
    else:
        return False