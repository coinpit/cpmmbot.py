from os.path import join
import logging

# Available levels: logging.(DEBUG|INFO|WARN|ERROR)
LOG_LEVEL = logging.INFO

COINPIT_URL = "http://localhost:9000/api/v1"
BITMEX_URL = "https://testnet.bitmex.com/api/v1/"

COINPIT_SYMBOL = 'BTCUSDW'
INTEREST_RATE = 0.06
COINPIT_TICK_SIZE = 1
COINPIT_QTY = 100
COINPIT_BITMEX_RATIO = 100
QUANTITY_MULTIPLIER = 5

# BITMEX_TOPICS=["instrument", "quote", "trade", "orderBook10", "order", "execution", "position" ]
BITMEX_TOPICS = ["instrument", "orderBook10", "order", "execution", "position"]
BITMEX_SYMBOL = 'XBTU17'
BITMEX_TRAILING_PEG = 2
HEDGE_INTERVAL=2 #in seconds



# copy api-key downloaded from coinpit. provide path.
COINPIT_API_FILE = 'ignore/moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU-c274ee8154f6b7ae.json'
# save bitmex api key file as json. example
# {
#   "ID": "Ag-_DuBvWrO8IK-6FnGhldzR",
#   "Secret": "_Dss0iITNH5-4QlCNYxqXQ7kA2ngSmhKX4tlRBdn4mmsR3_A"
# }
# provide path for the bitmex api key file.
BITMEX_API_FILE = 'ignore/bitmex_key.json'

