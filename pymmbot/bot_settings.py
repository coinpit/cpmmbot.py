from os.path import join
import logging

# Available levels: logging.(DEBUG|INFO|WARN|ERROR)
LOG_LEVEL = logging.INFO

COINPIT_SYMBOL = 'BTCUSDW'
INTEREST_RATE = 0.06
COINPIT_TICK_SIZE = 1
COINPIT_QTY = 100
COINPIT_BITMEX_RATIO = 100
QUANTITY_MULTIPLIER = 5

# BITMEX_TOPICS=["instrument", "quote", "trade", "orderBook10", "order", "execution", "position" ]
BITMEX_TOPICS = ["instrument", "orderBook10", "order", "execution", "position"]
BITMEX_SYMBOL = 'XBTU17'
BITMEX_TRAILING_PEG = 10
HEDGE_INTERVAL = 2  # in seconds
