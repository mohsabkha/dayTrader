from .ic_indicator import ic_indicator
from .vwap_indicator import vwap_indicator
from config import BOUGHT_MO, BOUGHT_GONZALO
#from alpaca.tradeBasic import create_order
import json
from datetime import datetime
def strats(message, websocket_ticker_data, data):
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
                if(len(websocket_ticker_data[x]['sym']) >= 53):
                    condition1 = ic_indicator(websocket_ticker_data[x], data)
                    condition2 = vwap_indicator(websocket_ticker_data[x])
                    condition3 = datetime.now().hour >= 8
                    condition4 = datetime.now().minute >= 31
                    if ( condition1 and condition2 and condition3 and condition4 and not BOUGHT_MO):
                        BOUGHT_MO = True
                        price = websocket_ticker_data[x]['close'][-1]
                        stop_loss = price - (.0515 * price)
                        take_profit = price + (.02 * price)
                        qty = 25000//price
                        side = 'buy'
                        #create_order(websocket_ticker_data[x]['sym'], qty, side, 'buy', 'gtc', take_profit, stop_loss)
                        #call alpaca
                        print('BUY WAS INITIATED')
            else:
                print(f':::LOOKING FOR SYMBOL:::')
        