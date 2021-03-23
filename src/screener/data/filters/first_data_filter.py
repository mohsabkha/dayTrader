####################################################################
#PURPOSE: to filter out the useless stocks using volume traded and price
#ARGS: list of data containing ticker symbols
#RETURNS: filtered list of data
#NOTE: n/a
#TO-DO: n/a
####################################################################
#filter by price and volume
def first_data_filter(data):
    print(':::::::::::::::::::FILTERING DATA BASED ON PRICE AND VOLUME')
    first_filter = []
    for x in range(len(data['symbol'])):
        if((data['close'][x] >= 5) and (data['close'][x] <= 100) and (data['volume'][x] >= 500000)):
            first_filter.append(data['symbol'][x])
    return first_filter