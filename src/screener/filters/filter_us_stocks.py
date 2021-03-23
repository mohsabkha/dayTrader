####################################################################
#PURPOSE: Filter tickers for those that are tradable on most commision free platforms (webull, robinhood, etc.)
#ARGS: tickers dataframe
#RETURNS: list of ticker names
#NOTE:
#TO-DO:
####################################################################
def filter_us_stocks(ticker_df):
    df = ticker_df[(ticker_df.currency == 'USD') & (ticker_df.locale == 'US')]
    exch = ['ARCA', 'NASDAQ', 'NYE']
    df = df[df['primaryExch'].isin(exch)]
    stockTypes = ['PFD', 'ADR', 'CEF', 'MLP', 'RIGHT', 'UNIT', 'WRT']
    df = df[df['type'].isin(stockTypes) == False]
    df.to_csv('polygon_tickers_us.csv')
    symbols = df.index.tolist()
    return symbols
