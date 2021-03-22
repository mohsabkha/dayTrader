import requests
import json
from config import *


ACCOUNT_URL = "{}/v2/account".format(APCA_API_BASE_URL_PAPER)
ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL_PAPER)

API_HEADERS = {
    "APCA-API-KEY-ID": APCA_API_KEY_ID, "APCA-API-SECRET-KEY": APCA_API_SECRET_KEY}


def get_account():
    r = requests.get(ACCOUNT_URL, headers=API_HEADERS)
    return json.loads(r.content)


# time_in_force, might want to use opg instead of gtc or day
def create_order(symbol, qty, side, type, time_in_force, take_profile, stop_loss):
    data = {
        "symbol": symbol, "qty": qty, "side": side, "type": type, "time_in_force": time_in_force, "take_profit": {
            "limit_price": "301"
        }, "stop_loss": stop_loss
    }
    r = requests.post(ORDERS_URL, json=data, headers=API_HEADERS)
    return json.loads(r.content)


def get_order():
    r = requests.get(ORDERS_URL, headers=API_HEADERS)
    return json.loads(r.content)


response = create_order('TSLA', 1, "buy", "market",
                        "gtc", {}, {"stop_price": '123', "limit_price": '123'})
print(response)

respone2 = get_order()
print(respone2)
