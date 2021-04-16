import pandas as pd
import os
####################################################################
# PURPOSE: extract individual tickers from pages
# ARGS: directory where pages of tickers are stored
# RETURNS: dataframe with tickers
# NOTE: n/a
# TO-DO: n/a
####################################################################


def combine_tickers(directory):
    df = pd.DataFrame()
    loading_counter = 0
    loading_animations = ['|', '/', '-', '\\']
    for f in os.listdir(directory):
        msg = ' loading minute data: ' + loading_animations[loading_counter]
        print(msg, end='\r')
        if(loading_counter == 3):
            loading_counter = 0
        else:
            loading_counter = loading_counter+1
        pathToCsv = os.path.join(directory, f)
        df2 = pd.read_csv(pathToCsv)
        df = df.append(df2)
    df.set_index('ticker', inplace=True)
    df.drop_duplicates()
    df.to_csv('polygon_tickers.csv')
    return df
