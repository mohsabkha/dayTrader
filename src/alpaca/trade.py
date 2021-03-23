import datetime
import threading

import alpaca_trade_api as tradeapi
import time
from alpaca_trade_api.rest import TimeFrame
from alpaca_trade_api.rest import APIError
from ...config import *  # should use env variables or add config to the git ignore

listOfAlpacaAccounts = []
gonzalo = {'apiKey': APCA_API_KEY_ID_GONZALO,
           'apiSecret': APCA_API_SECRET_KEY_GONZALO, 'baseUrl': APCA_API_BASE_URL_PAPER_GONZALO, 'limit': BUY_LIMIT_GONZALO}
mo = {'apiKey': APCA_API_KEY_ID_MO,
      'apiSecret': APCA_API_SECRET_KEY_MO, 'baseUrl': APCA_API_BASE_URL_PAPER_MO, "limit": BUY_LIMIT_MO}
listOfAlpacaAccounts.append(gonzalo)
# listOfAlpacaAccounts.append(mo)


class PurchaseStock:
    def __init__(self, API_KEY, API_SECRET, APCA_API_BASE_URL, listOfStocksToBuy, account_buying_limit):

        self.alpaca = tradeapi.REST(
            API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

        self.listOfStocksToBuy = listOfStocksToBuy
        self.account_buying_limit = account_buying_limit

    def run(self):
        # First, cancel any existing orders so they don't impact our buying power.
        orders = self.alpaca.list_orders(status="open")
        for order in orders:
            self.alpaca.cancel_order(order.id)
        # Get account info
        account_info = self.alpaca.get_account()
        print("Your account has $" + account_info.buying_power + " buying power")
        print("You're not a day trader yet" if account_info.pattern_day_trader else "Congrats you're a day trader")
        print("Your day trading count is " +
              str(account_info.daytrade_count) + ", not including today")
        print("Your day trading buying power is " +
              account_info.daytrading_buying_power + '\n')

        # Buy all stocks
        batchOrderResponse = []
        self.sendBatchOrder(self.listOfStocksToBuy,
                            account_info.buying_power, self.account_buying_limit, batchOrderResponse)

    # Submit a batch order that returns completed and uncompleted orders.

    def sendBatchOrder(self, stocks, buying_power, account_buying_limit, response):
        executed = []
        incomplete = []

        # Let's make sure we don't go past your set buying limit
        current_buying_power = 0.0
        if (float(account_buying_limit) >= float(buying_power)):
            current_buying_power = float(buying_power)
        else:
            current_buying_power = float(account_buying_limit)

        for stock in stocks:
            qty = current_buying_power//float(stock["price"])  # 10//3 = 3

            responseSubmitOrder = []
            tSubmitOrder = threading.Thread(target=self.submitOrder, args=[
                qty, stock["symbol"], 'buy', stock["take_profile_limit"], stock["stop_loss_price"], stock["stop_loss_price_limit"], responseSubmitOrder])
            tSubmitOrder.start()
            tSubmitOrder.join()
            if(not responseSubmitOrder[0]):
                # Stock order did not go through, add it to incomplete.
                incomplete.append(stock)
            else:
                executed.append(stock)
                current_buying_power = current_buying_power - \
                    qty*float(stock['price'])
            responseSubmitOrder.clear()

        response.append([executed, incomplete])

    # Submit an order if quantity is above 0.
    def submitOrder(self, qty, stock, side, take_profile_limit, stop_loss_price, stop_loss_price_limit, response):
        if(int(qty) > 0):
            try:
                self.alpaca.submit_order(
                    symbol=stock,
                    side=side,
                    type='market',
                    qty=qty,
                    time_in_force='day',
                    order_class='bracket',
                    take_profit=dict(
                        limit_price=take_profile_limit,
                    ),
                    stop_loss=dict(
                        stop_price=stop_loss_price,
                        limit_price=stop_loss_price_limit,
                    )
                )
                print("Market order of | " + str(qty) + " " +
                      stock + " " + side + " | completed.")
                response.append(True)
            # Catch API errors so it doesn't break our script
            except APIError as e:
                print("Market order of | " + str(qty) + " " + stock +
                      " " + side + " | did not go through. API returned " +
                      str(e.status_code) + " with: " + str(e))

                response.append(False)
        else:
            print("Quantity is 0, order of | " + str(qty) +
                  " " + stock + " " + side + " | not completed.")
            response.append(True)


# Run the PurchaseStock class
for account in listOfAlpacaAccounts:
    # TODO: get from algorithm.
    # Make sure stop_loss_price is lower than take_profile_limit
    # stop_loss_price_limit has to be lower than stop_loss_price
    stocksFromAlgorithm = []
    stocksFromAlgorithm.append(dict(
        symbol='TSLA',
        take_profile_limit='700.20',
        stop_loss_price='800.0',  # intentional error to test api error
        stop_loss_price_limit='649.0',
        price='652.20'
    ))
    stocksFromAlgorithm.append(dict(
        symbol='AAPL',
        take_profile_limit='130.02',
        stop_loss_price='110.02',
        stop_loss_price_limit='100.02',
        price='120.02'
    ))
    stocksFromAlgorithm.append(dict(
        symbol='GOOGL',
        take_profile_limit='3000',
        stop_loss_price='2000',
        stop_loss_price_limit='1800.0',
        price='2026.96'
    ))

    ps = PurchaseStock(account['apiKey'],
                       account['apiSecret'], account['baseUrl'], stocksFromAlgorithm, account['limit'])
    ps.run()
