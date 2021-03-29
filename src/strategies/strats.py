def strats(message, websocket_ticker_data, ic_data):
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
                    if (ic_indicator(websocket_ticker_data[x], ic_data) and vwap_indicator(websocket_ticker_data[x])):
                        #call alpaca
                        my_client.close_connection()
            else:
                print(f'Unknown Symbol Reported - {update['sym']} ::::::: CLOSING CONNECTION')
                my_client.close_connection()