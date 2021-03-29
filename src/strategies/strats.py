from .ic_indicator import ic_indicator
from .vwap_indicator import vwap_indicator
from config import BOUGHT_MO, BOUGHT_GONZALO
import json

def strats(message, websocket_ticker_data, ic_data):
    print(':::::::::::::::::::INTO MAIN BODY OF STRATS')
    message = json.loads(message)
    for update in message:
        print('received update from stock', update['sym'])
        for x in range(len(websocket_ticker_data)) :
            print('entered update')
            if(update['sym'] == websocket_ticker_data[x]['sym'][0]):
                print('organizing data from update\n')
                websocket_ticker_data[x]['sym'].append(update['sym'])
                websocket_ticker_data[x]['volume'].append(update['v'])
                websocket_ticker_data[x]['vwap'].append(update['a'])
                websocket_ticker_data[x]['high'].append(update['h'])
                websocket_ticker_data[x]['low'].append(update['l'])
                websocket_ticker_data[x]['close'].append(update['c'])
                websocket_ticker_data[x]['open'].append(update['o'])
                print(websocket_ticker_data)
                if(len(websocket_ticker_data[x]['sym']) >= 53):
                    condition1 = ic_indicator(websocket_ticker_data[x], ic_data)
                    condition2 = vwap_indicator(websocket_ticker_data[x])
                    if ( condition1 and condition2 and not BOUGHT_MO):
                        BOUGHT_MO = True
                        #call alpaca
                        print('BUY WAS INITIATED')
            else:
                print(f':::LOOKING FOR SYMBOL:::')
        