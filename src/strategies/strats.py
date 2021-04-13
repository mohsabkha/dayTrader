from .ic_indicator import ic_indicator
from .vwap_indicator import vwap_indicator
from config import *
from alpaca.trade import *
import json
from datetime import datetime

def strats(message, websocket_ticker_data, data):
    message = json.loads(message)
    for update in message:
        log_text = 'received update from stock ' + update['sym']
        f = open("./../logs.txt", "a")
        f.write(log_text)
        f.close()
        for x in range(len(websocket_ticker_data)) :
            if(update['sym'] == websocket_ticker_data[x]['sym'][0]):
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
                    #commented until further notice
                    # conditional for ic indicator
                    # if (condition1 and condition3 and condition4 and not BOUGHT_MUR):
                    #     BOUGHT_MUR = True
                    #     stock = [dict(
                    #         symbol = websocket_ticker_data[x]['sym'][-1],
                    #         price = websocket_ticker_data[x]['close'][-1],
                    #         stop_loss_price = price - (.0515 * price),
                    #         stop_loss_price_limit = price - (.1 * price),
                    #         take_profit_limit = price + (.02 * price))]
                    #     ps_mo = PurchaseStock(
                    #                 APCA_API_KEY_ID_MUR,
                    #                 APCA_API_SECRET_KEY_MUR,
                    #                 APCA_API_BASE_URL_PAPER_MUR, 
                    #                 stock, 
                    #                 BUY_LIMIT_MUR)
                    #     print(':::::::::::::::::::BUY WAS INITIATED FOR IC - MURAADS ACCOUNT SHOULD BE UPDATED')
                    # #conditional for vwap indicator
                    # if (condition2 and condition3 and condition4 and not BOUGHT_JAF):
                    #     BOUGHT_JAF = True
                    #     stock = dict(
                    #         symbol = websocket_ticker_data[x]['sym'][-1],
                    #         price = websocket_ticker_data[x]['close'][-1],
                    #         stop_loss_price = price - (.0515 * price),
                    #         stop_loss_price_limit = price - (.1 * price),
                    #         take_profit_limit = price + (.02 * price))
                    #     ps_mo = PurchaseStock(
                    #                 APCA_API_KEY_ID_JAF,
                    #                 APCA_API_SECRET_KEY_JAF,
                    #                 APCA_API_BASE_URL_PAPER_JAF, 
                    #                 stock, 
                    #                 BUY_LIMIT_JAF)
                    #     print(':::::::::::::::::::BUY WAS INITIATED FOR VWAP - JAAFERS ACCOUNT SHOULD BE UPDATED')
                    #conditional for vwap and ic indicators
                    if (condition2 and condition3 and condition4 and not BOUGHT_MO):
                        BOUGHT_MO = True
                        stock = [dict(
                            symbol = websocket_ticker_data[x]['sym'][-1],
                            price = str(round(websocket_ticker_data[x]['close'][-1],3)),
                            stop_loss_price = str(round(price - (.0515 * price),3)),
                            stop_loss_price_limit = str(round(price - (.1 * price),3)),
                            take_profit_limit = str(round(price + (.02 * price),3)))]
                        ps_mo = PurchaseStock(
                                    APCA_API_KEY_ID_MO,
                                    APCA_API_SECRET_KEY_MO,
                                    APCA_API_BASE_URL_PAPER_MO, 
                                    stock, 
                                    BUY_LIMIT_MO)
                        print(':::::::::::::::::::BUY WAS INITIATED FOR BOTH VWAP AND IC - MOHAMMADS ACCOUNT SHOULD BE UPDATED')
        