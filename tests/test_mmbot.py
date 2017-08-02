import pytest
import unittest
import json
from pymmbot import mmbot
from time import sleep


class Test(unittest.TestCase):
    def setUp(self):
        self.apikey = {
            "name"         : "972b95651681cf63",
            "role"         : "trade",
            "apiPublicKey" : "972b95651681cf63a7c4c01ff3c4fadb26c8a42e9cb38edc26294d0375213550",
            "userid"       : "moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU",
            "secretKey"    : "e339701456f656fc42356c44934772651e07b1a04212bba9837654b26fe4eb5e972b95651681cf63a7c4c01ff3c4fadb26c8a42e9cb38edc26294d0375213550",
            "authorization": "IMXlbendaVlsXNPyDmcboNGTh/N0LAPoU01LOlPNdDT/L3jGJm9BSeMvNvg9cYi3a46/qN6C4ThvXRuLqnQFtTI=",
            "serverAddress": "n3kKyhxAU6n9MLWto9rew89dB5ghgZSbbr",
            "accountid"    : "2NGJqK6fXWfMMtJwWHdKT59WzqKDxFKagJp",
            "publicKey"    : "02d324e7149836c05b66ae4d51ac1a708afb0ab6b72839bcbda14d1f246fb04828"
        }

    def test_connect_coinpit_socket(self):
        print(self.apikey['name'])
        bot = mmbot.MMBot(self.apikey)
        bot.connect('http://localhost:9000')

    def test_send_on_socket(self):
        bot = mmbot.MMBot(self.apikey)
        bot.connect('http://localhost:9000')
        bot.subscribe()
        # bot.loop()
        # bot.send(message)

    def test_register(self):
        bot = mmbot.MMBot(self.apikey)
        bot.connect('http://localhost:9000')
        bot.subscribe()
        bot.register()
        bot.loop()


    def test_get_headers(self):
        apikey = {
            "name"         : "18e5f6966c901e78",
            "role"         : "trade",
            "apikey"       : "18e5f6966c901e78f5946bfdd798981559e8df0be73d746d90a458779fddc05b",
            "userid"       : "msupsAQFexFrGpfrxXGSvNUqUwNRRwSc3s",
            "secretKey"    : "d31448736fcc6945f4482e95055f9ecb898bc3ce166da8121939529101eff1b118e5f6966c901e78f5946bfdd798981559e8df0be73d746d90a458779fddc05b",
            "authorization": "HxwFaJHLAqu/KxaOhIe11KXZP2/L6CHFKk5AxLk8vdg0WAQj6EovVGTftd35+gsTgMn/uZJqDf1fK3SGghRYQeU="
        }
        method = "POST"
        body = [
            {
                "userid"     : "msupsAQFexFrGpfrxXGSvNUqUwNRRwSc3s",
                "side"       : "sell",
                "quantity"   : 1,
                "price"      : 1700.8,
                "orderType"  : "LMT",
                "clientid"   : "9764b759-53b9-4a71-8591-78cf18dbe616",
                "stopPrice"  : 15.7,
                "crossMargin": False,
                "targetPrice": "NONE",
                "postOnly"   : False,
                "instrument" : "MBTCUSD7K090310"
            }
        ]
        uri = "/order"
        nonce = "1494299047138"
        result = "SIGN msupsAQFexFrGpfrxXGSvNUqUwNRRwSc3s.18e5f6966c901e78:20HXdTmvzU8IX0tYpPmTHTMADQkKdxpwPT7bd/hqQ9ewXAQ2QxMuKnS5NULyVu7IkWIjgTTqHbIXxge/mFSEAA=="
        bot = mmbot.MMBot(apikey)
        headers = bot.get_headers(apikey['userid'], apikey['name'], apikey['secretKey'], nonce, method, uri, body)
        self.assertEquals(headers["Authorization"], result)
