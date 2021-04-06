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
# Gonzalo - 5 trades based on screener
APCA_API_KEY_ID_GONZALO = "PKQRKQYQTE7RG9QQLCGQ"
APCA_API_SECRET_KEY_GONZALO = "iUTMGWS5ZuQVybsB8WrE74AEdpeUyt5qqh1BnThl"
APCA_API_BASE_URL_PAPER_GONZALO = "https://paper-api.alpaca.markets"
BUY_LIMIT_GONZALO = '25000'
BOUGHT_GONZALO = False
# Muraad - 1 trade based on screener
APCA_API_KEY_ID_MUR = "your key here"
APCA_API_SECRET_KEY_MUR = "your key here"
APCA_API_BASE_URL_PAPER_MUR = "https://paper-api.alpaca.markets"
BUY_LIMIT_KEV = '25000'
BOUGHT_MUR = False
# Jaafer - 1 trade based on IC strat
APCA_API_KEY_ID_JAF = "PKVAAXXOYV4JY2ASJKNV"
APCA_API_SECRET_KEY_JAF = "tpvLSxGtLlIshudqxChLY2gfQfd98OQ8yYwJalcY"
APCA_API_BASE_URL_PAPER_JAF = "https://paper-api.alpaca.markets"
BUY_LIMIT_JAF = '25000'
BOUGHT_JAF = False
# Sameer - 1 trade based on VWAP strat
APCA_API_KEY_ID_SAM = "PKGBHOSGRBVHGP7L8M4R"
APCA_API_SECRET_KEY_SAM = "VCSyNX2kofcRsQC25RV95sH6QtuZrtrvWJwuzDVI"
APCA_API_BASE_URL_PAPER_SAM = "https://paper-api.alpaca.markets"
BUY_LIMIT_SAM = '25000'
BOUGHT_SAM = False
# Mohammad - 1 trade based on all strats
APCA_API_KEY_ID_MO = "PKM6MR6GJO5BAZ1H99J0"
APCA_API_SECRET_KEY_MO = "tkYetTY8oZEZoCHv66QfOmMFI4lG6N731wQX13j7"
APCA_API_BASE_URL_PAPER_MO = "https://paper-api.alpaca.markets"
BUY_LIMIT_MO = '25000'
BOUGHT_MO = False
# APCA_API_BASE_URL_LIVE = "https://api.alpaca.markets"

# Used for tradeBasic.py
APCA_API_KEY_ID = "your key here"
APCA_API_SECRET_KEY = "your key here"
APCA_API_BASE_URL_PAPER = "https://paper-api.alpaca.markets"

#this is an alternative to the other code
ACCOUNTS = {
    'alpaca_base_url' : 'https://api.alpaca.markets',
    'alpaca_paper_url' : 'https://paper-api.alpaca.markets',
    'accounts':[
        {
            'first_name': 'GONZALO',
            'last_name': 'PANTOJA',
            'api_key': 'PKQRKQYQTE7RG9QQLCGQ',
            'secret_key': 'iUTMGWS5ZuQVybsB8WrE74AEdpeUyt5qqh1BnThl',
            'buy_power' : '25000'
        },
        {
            'first_name': 'MOHAMMAD',
            'last_name': 'KHAN',
            'api_key': 'PKM6MR6GJO5BAZ1H99J0',
            'secret_key': 'tkYetTY8oZEZoCHv66QfOmMFI4lG6N731wQX13j7',
            'buy_power' : '25000'
        },
        {
            'first_name': 'JAAFER',
            'last_name': 'MONSOUR',
            'api_key': 'PKVAAXXOYV4JY2ASJKNV',
            'secret_key': 'tpvLSxGtLlIshudqxChLY2gfQfd98OQ8yYwJalcY',
            'buy_power' : '25000'
        },
        {
            'first_name': 'SAMEER',
            'last_name': 'TARIQ',
            'api_key': 'PKGBHOSGRBVHGP7L8M4R',
            'secret_key': 'VCSyNX2kofcRsQC25RV95sH6QtuZrtrvWJwuzDVI',
            'buy_power' : '25000'
        },
        {
            'first_name': 'MURAAD',
            'last_name': 'KHAN',
            'api_key': '',
            'secret_key': '',
            'buy_power' : '25000'
        }
    ]
}










