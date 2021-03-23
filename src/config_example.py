#below is used by polygon and screener code
from screener.retreive_data.get_date import get_date
KEY = 'your polygon key here'
POLYGON_URL = 'https://api.polygon.io'
POLYGON_TICKER_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'#page,key
POLYGON_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?unadjusted=true&apiKey={}'#ticker,start,end,key
POLYGON_DIV_URL = 'https://api.polygon.io/v2/reference/dividends/{}?apiKey={}'#ticker,key
POLYGON_SPLIT_URL = 'https://api.polygon.io/v2/reference/splits/{}?apiKey={}'#ticker,key
POLYGON_TYPES_URL = 'https://api.polygon.io/v2/reference/types?apiKey={}'#key
POLYGON_OPEN_CLOSE_URL = 'https://api.polygon.io/v1/open-close/{}/{}?unadjusted=true&apiKey={}'#ticker,date,key
POLYGON_AGGS_MINUTE_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}?unadjusted=true&sort=desc&limit=360&apiKey={}'#ticker,date,date,key
START = 'YYYY-MM-DD'
CLOSING_TIME, END = get_date('YYYY-MM-DD')
TICKER_PAGE_PATH = '\\polygon_data\\tickers'

# Below is used for alpaca code
# Gonzalo
APCA_API_KEY_ID_GONZALO = "your key here"
APCA_API_SECRET_KEY_GONZALO = "your key here"
APCA_API_BASE_URL_PAPER_GONZALO = "https://paper-api.alpaca.markets"
BUY_LIMIT_GONZALO = '5000'
# Mo
APCA_API_KEY_ID_MO = "PKM6MR6GJO5BAZ1H99J0"
APCA_API_SECRET_KEY_MO = "tkYetTY8oZEZoCHv66QfOmMFI4lG6N731wQX13j7"
APCA_API_BASE_URL_PAPER_MO = "https://paper-api.alpaca.markets"
BUY_LIMIT_MO = '25000'
# APCA_API_BASE_URL_LIVE = "https://api.alpaca.markets"


# Used for tradeBasic.py
APCA_API_KEY_ID = "your key here"
APCA_API_SECRET_KEY = "your key here"
APCA_API_BASE_URL_PAPER = "https://paper-api.alpaca.markets"


