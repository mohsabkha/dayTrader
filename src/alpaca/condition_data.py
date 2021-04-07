import pandas as pd
#   stocksFromAlgorithm.append(dict(
#         symbol='TSLA',
#         take_profile_limit='700.20',
#         stop_loss_price='800.0',  # intentional error to test api error
#         stop_loss_price_limit='649.0',
#         price='652.20'
#     ))


def condition_data(dataframe):
    buy_list = []
    alpaca_list = {'stock': [], 'stop_loss': [], 'stop_loss_limit': [], 'take_profit_limit': [], 'price': [], 'volume': [], 'score': []}
    for ticker in dataframe.index:
        stop_loss = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .0515
        stop_loss_limit = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .06
        take_profit_limit = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .02
        buy_list.append(dict(
            symbol=str(ticker),
            take_profile_limit=str(take_profit_limit),
            stop_loss_price=str(stop_loss),\
            stop_loss_price_limit=str(stop_loss_limit),
            price=str(dataframe['Closing Price'][ticker])
        ))
        alpaca_list['stock'].append(str(ticker))
        alpaca_list['stop_loss'].append(str(stop_loss))
        alpaca_list['stop_loss_limit'].append(str(stop_loss_limit))
        alpaca_list['take_profit_limit'].append(str(take_profit_limit))
        alpaca_list['price'].append(str(dataframe['Closing Price'][ticker]))
        alpaca_list['volume'].append(str(dataframe['Volume'][ticker]))
        alpaca_list['score'].append(str(dataframe['Score'][ticker]))
    return (pd.DataFrame(alpaca_list), buy_list)