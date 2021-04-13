def vwap_indicator(ticker_values):
    #if open is lower than vwap and close is higher
    if (ticker_values['open'][-1] < ticker_values['vwap'][-1]  and ticker_values['close'][-1] > ticker_values['vwap'][-1]):
        print(':::::::::::::::::::VWAP INDICATOR RETURNED TRUE')
        return True
    else:
        return False