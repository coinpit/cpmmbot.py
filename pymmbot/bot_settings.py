from os.path import join
import logging

# Available levels: logging.(DEBUG|INFO|WARN|ERROR)
LOG_LEVEL = logging.INFO

# instrument used for coinpit
COINPIT_SYMBOL = 'BTCUSDW'
# insterest rate used. this will be added as offset from index price.
INTEREST_RATE = 0.06
# decimal paces supported by coinpit instrument
COINPIT_TICK_SIZE = 1
# market maker on coinpit will maintain number of contracts on buy and sell side
COINPIT_QTY = 100
# 1 contract at coinpit is equal to 100 contracts on bitmex
COINPIT_BITMEX_RATIO = 100
# spread from bitmex is calculated for quantity. quantity = COINPIT_QTY * COINPIT_BITMEX_RATIO * QUANTITY_MULTIPLIER
QUANTITY_MULTIPLIER = 5
# one buy and one sell order is placed 2% away from index to make sure that there is always some spread is avalable.
COINPIT_LATCH = 0.02

# BITMEX_TOPICS=["instrument", "quote", "trade", "orderBook10", "order", "execution", "position" ]
BITMEX_TOPICS = ["instrument", "orderBook10", "order", "execution", "position"]
BITMEX_SYMBOL = 'XBTUSD'
# places a trailing stop order with peg. if this value is 0, a market order will be placed.
BITMEX_TRAILING_PEG = 10
# BITMEX_TRAILING_PEG = 0

HEDGE_INTERVAL = 2  # in seconds
