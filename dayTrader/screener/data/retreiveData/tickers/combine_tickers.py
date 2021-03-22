
####################################################################
#PURPOSE: extract individual tickers from pages
#ARGS: directory where pages of tickers are stored
#RETURNS: dataframe with tickers
#NOTE: n/a
#TO-DO: n/a
####################################################################
def combine_tickers(directory):
    df = pd.DataFrame()
    for f in os.listdir(directory):
        df2 = pd.read_csv("{}/{}".format(directory, f))
        df = df.append(df2)
    df.set_index('ticker', inplace=True)
    df.drop_duplicates()
    df.to_csv('polygon_tickers.csv')
    return df
