import unittest

from pymmbot.coinpit import crypto


class Test(unittest.TestCase):
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
        result = "SIGN msupsAQFexFrGpfrxXGSvNUqUwNRRwSc3s.18e5f6966c901e78:4yE0+ECUb5YWNLv5r0DL6/GChi/aATmAk77u+CnDSXg0TYf0gW3L+YZ6Mq3jWuccmGV61vjOAyB+Eya7HDK5DA=="
        auth = crypto.get_auth(apikey['userid'], apikey['name'], apikey['secretKey'], nonce, method, uri, body)
        self.assertEquals(auth, result)
