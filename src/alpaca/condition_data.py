import pandas as pd

def condition_data(dataframe):
    alpaca_list = {'stock': [], 'stop_loss': [], 'stop_loss_limit': [], 'take_profit_limit': [], 'price': [], 'volume': [], 'score': []}
    for ticker in dataframe.index:
        stop_loss = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .0515
        stop_loss_limit = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .06
        take_profit_limit = dataframe['Closing Price'][ticker] - dataframe['Closing Price'][ticker] * .02
        alpaca_list['stock'].append(str(ticker))
        alpaca_list['stop_loss'].append(str(stop_loss))
        alpaca_list['stop_loss_limit'].append(str(stop_loss_limit))
        alpaca_list['take_profit_limit'].append(str(take_profit_limit))
        alpaca_list['price'].append(dataframe['Closing Price'][ticker])
        alpaca_list['volume'].append(dataframe['Volume'][ticker])
        alpaca_list['score'].append(dataframe['Score'][ticker])
    return pd.DataFrame(alpaca_list)