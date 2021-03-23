from .get_date import get_date

KEY = 'your key here' #Polygon key goes here
#POLYGON_URL = 'https://api.polygon.io'
POLYGON_TICKER_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'#page,key
POLYGON_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?unadjusted=true&apiKey={}'#ticker,start,end,key
#POLYGON_DIV_URL = 'https://api.polygon.io/v2/reference/dividends/{}?apiKey={}'#ticker,key
#POLYGON_SPLIT_URL = 'https://api.polygon.io/v2/reference/splits/{}?apiKey={}'#ticker,key
#POLYGON_TYPES_URL = 'https://api.polygon.io/v2/reference/types?apiKey={}'#key
POLYGON_OPEN_CLOSE_URL = 'https://api.polygon.io/v1/open-close/{}/{}?unadjusted=true&apiKey={}'#ticker,date,key
POLYGON_AGGS_MINUTE_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}?unadjusted=true&sort=desc&limit=360&apiKey={}'#ticker,date,date,key
START = 'YYYY-MM-DD'
CLOSING_TIME, END = get_date('YYYY-MM-DD')
TICKER_PAGE_PATH = '\\data\\tickers'