import pytest
import unittest
import json
from pymmbot import mmbot
import common_util
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

    def test_register(self):
        bot = mmbot.MMBot()
        bot.connect_coinpit('http://localhost:9000/api/v1', self.apikey)
        bot.update_client_cache()
        common_util.loop()
