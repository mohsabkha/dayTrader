from .ic_indicator import ic_indicator
from .vwap_indicator import vwap_indicator


def strats(message, websocket_ticker_data, ic_data, my_client):
    print(message)
    for update in message:
        for x in range(len(websocket_ticker_data)) :
            if(update['sym'] == websocket_ticker_data[x]['sym'][0]):
                websocket_ticker_data[x]['sym'].append(message[update]['sym'])
                websocket_ticker_data[x]['volume'].append(message[update]['v'])
                websocket_ticker_data[x]['vwap'].append(message[update]['a'])
                websocket_ticker_data[x]['high'].append(message[update]['h'])
                websocket_ticker_data[x]['low'].append(message[update]['l'])
                websocket_ticker_data[x]['close'].append(message[update]['c'])
                websocket_ticker_data[x]['open'].append(message[update]['o'])
                if(len(websocket_ticker_data[x]['sym']) >= 53):
                    condition1 = ic_indicator(websocket_ticker_data[x], ic_data)
                    condition2 = vwap_indicator(websocket_ticker_data[x])
                    if ( condition1 and condition2 ):
                        #call alpaca
                        my_client.close_connection()
            else:
                print(f'Unknown Symbol Reported - {update['sym']} ::::::: CLOSING CONNECTION')
                my_client.close_connection()