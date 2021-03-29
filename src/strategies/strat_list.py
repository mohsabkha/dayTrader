# this gets data, transforms it in order to be able to calculate information relavent to the strategies and returns a list that is readable by the websocket
def strat_list(stock_data):
    ic_data = {'conversion_line':[], 'base_line':[], 'lead_A':[], 'lead_B':[], 'lag_span':[]} 
    websocket_ticker_data = [
        {'sym':[], 'volume':[], 'vwap':[], 'high':[], 'low':[], 'close':[], 'open':[]},
        {'sym':[], 'volume':[], 'vwap':[], 'high':[], 'low':[], 'close':[], 'open':[]},
        {'sym':[], 'volume':[], 'vwap':[], 'high':[], 'low':[], 'close':[], 'open':[]},
        {'sym':[], 'volume':[], 'vwap':[], 'high':[], 'low':[], 'close':[], 'open':[]},
        {'sym':[], 'volume':[], 'vwap':[], 'high':[], 'low':[], 'close':[], 'open':[]}
    ]
    websocket_symbols = []
    count = 0
    for ticker in stock_score.index:
        websocket_symbols.append(f'A.{ticker}')
        websocket_ticker_data[count]['sym'].append(ticker)
        count += 1
    return (websocket_symbols, websocket_ticker_data, ic_data)