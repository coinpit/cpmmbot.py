# bitmex api key. This is sample. change with your bitmex api key and secret
BITMEX_API_KEY = 'Ag-_DuBvWrO8IK-6FnGhldzR'
BITMEX_API_SECRET = '_Dss0iITNH5-4QlCNYxqXQ7kA2ngSmhKX4tlRBdn4mmsR3_A'

# coinpit api key. This is sample api key. copy api key content downloaded from coinpit.
COINPIT_API_KEY = {
    "name"         : "c274ee8154f6b7ae",
    "role"         : "trade",
    "apiPublicKey" : "c274ee8154f6b7ae26f83959ebe8a8408f4c8f26e4a2a67aa1183d67855b4923",
    "userid"       : "moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU",
    "secretKey"    : "e41e7e05d72474d315835f9aaa611c4538b70cd9f0da3af8ca5348442c02a01ec274ee8154f6b7ae26f83959ebe8a8408f4c8f26e4a2a67aa1183d67855b4923",
    "authorization": "H035g/EV91qkp8R9SEXaEoCO/6HlNdvYXcBZWgfzmeDzbSIfbdQjq7XTbj/8AO1HbSdNOREC1abFQBehkKk1HiY=",
    "serverAddress": "n3kKyhxAU6n9MLWto9rew89dB5ghgZSbbr",
    "accountid"    : "2NGJqK6fXWfMMtJwWHdKT59WzqKDxFKagJp",
    "publicKey"    : "02d324e7149836c05b66ae4d51ac1a708afb0ab6b72839bcbda14d1f246fb04828"
}

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

BITMEX_SYMBOL = 'XBTUSD'
# places a trailing stop order with peg. if this value is 0, a market order will be placed.
BITMEX_TRAILING_PEG = 10
# BITMEX_TRAILING_PEG = 0

HEDGE_INTERVAL = 2  # in seconds
