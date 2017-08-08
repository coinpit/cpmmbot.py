import unittest

from pymmbot import mmbot
from utils import common_util
import sinon
from settings import settings
from freezegun import freeze_time
from bitmex import bitmex


class Test(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None


    def test_bitmex_order(self):
        bm = bitmex.Bitmex()
        bm.place_order(23, 'Buy', 2)

    def test_start(self):
        bot = mmbot.MMBot()
        bot.connect_coinpit()
        # bot.get_account_details()
        bot.connect_bitmex()
        common_util.loop()

    def test_update_orders(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q04'     : {}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {},
                                               'BTCUSD7Q11'     : {}, 'MBTCUSD7Q032110': {
                '86e21770-788f-11e7-9c8d-e068e3ff2d24': {'uuid'        : '86e21770-788f-11e7-9c8d-e068e3ff2d24',
                                                         'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                         'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                         'cancelled'   : 0, 'price': 2778.2, 'normalizedPrice': 3599453,
                                                         'averagePrice': 0, 'entryTime': 1501794359525912,
                                                         'eventTime'   : 1501794349671889, 'status': 'open',
                                                         'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                         'clientid'    : '9b806e9e-9b16-4f66-916a-c99747ec530b',
                                                         'instrument'  : 'MBTCUSD7Q032110', 'commission': 0.0005,
                                                         'reward'      : 0, 'cushion': 5, 'reservedTicks': 2,
                                                         'crossMargin' : False, 'marginPerQty': 71951}},
                                               'MBTCUSD7Q032115': {}}, 'positions': {}, 'margin': 63020588,
                                    'displayMargin': 63020588, 'accountMargin': 63092539,
                                    'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        data = {'result'                                                   : [
            {'uuid'           : '86e21770-788f-11e7-9c8d-e068e3ff2d24', 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
             'side'           : 'buy', 'quantity': 1, 'filled': 0, 'cancelled': 0, 'price': 2775.1,
             'normalizedPrice': 3603474, 'averagePrice': 0, 'entryTime': 1501794440492276,
             'eventTime'      : 1501794349671889, 'status': 'open', 'entryOrder': {}, 'orderType': 'LMT',
             'targetPrice'    : 'NONE', 'clientid': '9b806e9e-9b16-4f66-916a-c99747ec530b',
             'instrument'     : 'MBTCUSD7Q032110', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
             'crossMargin'    : False, 'marginPerQty': 71951}], 'requestid': 'acb1fd34-6748-4cf2-88cc-9f214d651b77'}

        bot.on_order_update(data)
        self.assertEquals(bot.coinpit_user_details['orders']['MBTCUSD7Q032110']['86e21770-788f-11e7-9c8d-e068e3ff2d24'],
                          data['result'][0])

    def test_add_order(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {
            'orders': {'BTCUSD7Q04'     : {}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {}, 'BTCUSD7Q11': {},
                       'MBTCUSD7Q032245': {}, 'MBTCUSD7Q032250': {}}, 'positions': {}, 'margin': 63092539,
            'displayMargin': 63092539, 'accountMargin': 63092539, 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        data = {'result'                                                   : [
            {'uuid'           : '312ab310-789d-11e7-a2c0-245668e150b8', 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
             'side'           : 'buy', 'quantity': 1, 'filled': 0, 'cancelled': 0, 'price': 2786.9,
             'normalizedPrice': 3588216, 'averagePrice': 0, 'entryTime': 1501800218817209,
             'eventTime'      : 1501800218817209, 'status': 'open', 'entryOrder': {}, 'orderType': 'LMT',
             'targetPrice'    : 'NONE', 'clientid': '4433dda4-8cfa-4d9c-a0c0-9384ac39a46c',
             'instrument'     : 'MBTCUSD7Q032245', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
             'crossMargin'    : False, 'marginPerQty': 71984}], 'requestid': 'a8de9b2c-f798-4e4a-97d2-bf52d4299144'}
        bot.on_order_add(data)
        self.assertEquals(bot.coinpit_user_details['orders']['MBTCUSD7Q032245']['312ab310-789d-11e7-a2c0-245668e150b8'],
                          data['result'][0])

    def test_on_del_order(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q04'                               : {
            'e0cbc2c0-78a0-11e7-8f0b-af48c26f303c': {'uuid'        : 'e0cbc2c0-78a0-11e7-8f0b-af48c26f303c',
                                                     'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                     'cancelled'   : 0, 'price': 2786, 'normalizedPrice': 3589375,
                                                     'averagePrice': 0, 'entryTime': 1501801801964422,
                                                     'eventTime'   : 1501801801964422, 'status': 'open',
                                                     'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                     'clientid'    : '88736c7e-86f8-49e0-b982-cfdd4a6d8bbe',
                                                     'instrument'  : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0,
                                                     'cushion'     : 5, 'reservedTicks': 2, 'crossMargin': False,
                                                     'marginPerQty': 72297}}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {},
            'BTCUSD7Q11'                                                                  : {},
            'MBTCUSD7Q032315'                                                             : {},
            'MBTCUSD7Q032320'                                                             : {}}, 'positions': {},
            'margin': 63020242, 'displayMargin': 63020242, 'accountMargin': 63092539,
            'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        data = {'result': ['e0cbc2c0-78a0-11e7-8f0b-af48c26f303c'], 'requestid': '761a344d-90a9-46d2-88bd-acc94e427cde'}
        bot.on_order_del(data)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['e0cbc2c0-78a0-11e7-8f0b-af48c26f303c'],
                          None)

    def test_on_patch_remove(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q04'                               : {
            'ae9f7701-78a6-11e7-a227-8a95d7daff8a': {'uuid'        : 'ae9f7701-78a6-11e7-a227-8a95d7daff8a',
                                                     'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                     'cancelled'   : 0, 'price': 2780.5, 'normalizedPrice': 3596475,
                                                     'averagePrice': 0, 'entryTime': 1501804294768699,
                                                     'eventTime'   : 1501804294768699, 'status': 'open',
                                                     'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                     'clientid'    : 'e506b9fa-6f4a-40da-88d7-256091a373fa',
                                                     'instrument'  : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0,
                                                     'cushion'     : 5, 'reservedTicks': 2, 'crossMargin': False,
                                                     'marginPerQty': 72496},
            'aef3d890-78a6-11e7-a41b-7d28c691bc0c': {'uuid'        : 'aef3d890-78a6-11e7-a41b-7d28c691bc0c',
                                                     'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                     'cancelled'   : 0, 'price': 2777.6, 'normalizedPrice': 3600230,
                                                     'averagePrice': 0, 'entryTime': 1501804295321335,
                                                     'eventTime'   : 1501804295321335, 'status': 'open',
                                                     'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                     'clientid'    : '99b16972-f3fb-41d6-86bc-361677171e09',
                                                     'instrument'  : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0,
                                                     'cushion'     : 5, 'reservedTicks': 2, 'crossMargin': False,
                                                     'marginPerQty': 72496}}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {},
            'BTCUSD7Q11'                                                                  : {},
            'MBTCUSD7Q032355'                                                             : {},
            'MBTCUSD7Q040000'                                                             : {}}, 'positions': {},
            'margin': 62947547, 'displayMargin': 62947547, 'accountMargin': 63092539,
            'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        data = {'result'   : [{'op'        : 'remove',
                               'response'  : [
                                   'aef3d890-78a6-11e7-a41b-7d28c691bc0c', 'ae9f7701-78a6-11e7-a227-8a95d7daff8a'],
                               'statusCode': 200}],
                'requestid': 'fce2416c-b1cd-4307-9127-1e23dacae5c0'}
        bot.on_order_patch(data)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['ae9f7701-78a6-11e7-a227-8a95d7daff8a'],
                          None)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['aef3d890-78a6-11e7-a41b-7d28c691bc0c'],
                          None)

    def test_on_patch_add(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q04'                               : {
            'ae9f7701-78a6-11e7-a227-8a95d7daff8a': {'uuid'        : 'ae9f7701-78a6-11e7-a227-8a95d7daff8a',
                                                     'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                     'cancelled'   : 0, 'price': 2780.5, 'normalizedPrice': 3596475,
                                                     'averagePrice': 0, 'entryTime': 1501804294768699,
                                                     'eventTime'   : 1501804294768699, 'status': 'open',
                                                     'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                     'clientid'    : 'e506b9fa-6f4a-40da-88d7-256091a373fa',
                                                     'instrument'  : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0,
                                                     'cushion'     : 5, 'reservedTicks': 2, 'crossMargin': False,
                                                     'marginPerQty': 72496},
            'aef3d890-78a6-11e7-a41b-7d28c691bc0c': {'uuid'        : 'aef3d890-78a6-11e7-a41b-7d28c691bc0c',
                                                     'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'        : 'buy', 'quantity': 1, 'filled': 0,
                                                     'cancelled'   : 0, 'price': 2777.6, 'normalizedPrice': 3600230,
                                                     'averagePrice': 0, 'entryTime': 1501804295321335,
                                                     'eventTime'   : 1501804295321335, 'status': 'open',
                                                     'entryOrder'  : {}, 'orderType': 'LMT', 'targetPrice': 'NONE',
                                                     'clientid'    : '99b16972-f3fb-41d6-86bc-361677171e09',
                                                     'instrument'  : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0,
                                                     'cushion'     : 5, 'reservedTicks': 2, 'crossMargin': False,
                                                     'marginPerQty': 72496}}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {},
            'BTCUSD7Q11'                                                                  : {},
            'MBTCUSD7Q032355'                                                             : {},
            'MBTCUSD7Q040000'                                                             : {}}, 'positions': {},
            'margin': 62947547, 'displayMargin': 62947547, 'accountMargin': 63092539,
            'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        data = {'result'   : [{'op'        : 'remove',
                               'response'  : [
                                   'aef3d890-78a6-11e7-a41b-7d28c691bc0c', 'ae9f7701-78a6-11e7-a227-8a95d7daff8a'],
                               'statusCode': 200}],
                'requestid': 'fce2416c-b1cd-4307-9127-1e23dacae5c0'}
        bot.on_order_patch(data)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['ae9f7701-78a6-11e7-a227-8a95d7daff8a'],
                          None)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['aef3d890-78a6-11e7-a41b-7d28c691bc0c'],
                          None)

    def test_on_patch_add_update(self):
        add = {'result'   : [{'op'                                         : 'add', 'response': [
            {'uuid'           : '16f9d6f0-78b7-11e7-ab45-084d643d5866', 'userid': 'miqHcgxszTkcaQggGoK4MYDPekTeutihMA',
             'side'           : 'buy', 'quantity': 5, 'filled': 0, 'cancelled': 0, 'price': 2781.3,
             'normalizedPrice': 3595441, 'averagePrice': 0, 'entryTime': 1501811341791395,
             'eventTime'      : 1501811341791395, 'status': 'open', 'entryOrder': {}, 'orderType': 'LMT',
             'stopPrice'      : 50, 'targetPrice': 'NONE', 'clientid': 'caa14e76-f09d-4275-a726-f96b24fcae91',
             'instrument'     : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
             'crossMargin'    : True, 'marginPerQty': 74075}], 'statusCode': 200}],
               'requestid': '39d2c0df-bf87-4fb1-b10d-0597d88dfa46'}
        replace = {'result'   : [{'op'                                     : 'replace', 'response': [
            {'uuid'           : '16f9d6f0-78b7-11e7-ab45-084d643d5866', 'userid': 'miqHcgxszTkcaQggGoK4MYDPekTeutihMA',
             'side'           : 'buy', 'quantity': 5, 'filled': 0, 'cancelled': 0, 'price': 2779,
             'normalizedPrice': 3598417, 'averagePrice': 0, 'entryTime': 1501811343606342,
             'eventTime'      : 1501811341791395, 'status': 'open', 'entryOrder': {}, 'orderType': 'LMT',
             'stopPrice'      : 50, 'targetPrice': 'NONE', 'clientid': 'caa14e76-f09d-4275-a726-f96b24fcae91',
             'instrument'     : 'BTCUSD7Q04', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
             'crossMargin'    : True, 'marginPerQty': 74075}], 'statusCode': 200}],
                   'requestid': '7736069f-7676-4ac0-aef1-153009d28b5a'}
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {
            'orders': {'BTCUSD7Q04'     : {}, 'BCHBTC7Q11': {}, 'BCHBTC7Q04': {}, 'BTCUSD7Q11': {},
                       'MBTCUSD7Q040150': {}, 'MBTCUSD7Q040155': {}}, 'positions': {}, 'margin': 23479383,
            'displayMargin': 23479383, 'accountMargin': 23479383, 'userid': 'miqHcgxszTkcaQggGoK4MYDPekTeutihMA'}

        bot.on_order_patch(add)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['16f9d6f0-78b7-11e7-ab45-084d643d5866'],
                          add['result'][0]['response'][0])

        bot.on_order_patch(replace)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['16f9d6f0-78b7-11e7-ab45-084d643d5866'],
                          replace['result'][0]['response'][0])

    def test_on_patch_split(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {
            'orders': {'BTCUSD7Q04': {
                'e4030c10-78b8-11e7-b7bb-1404f32a4ed5': {'uuid'                : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                                         'userid'              : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                         'side'                : 'sell',
                                                         'quantity'            : 4,
                                                         'filled'              : 0,
                                                         'cancelled'           : 0,
                                                         'price'               : 2734.2,
                                                         'normalizedPrice'     : 3657377,
                                                         'averagePrice'        : 0,
                                                         'entryTime'           : 1501812115281754,
                                                         'eventTime'           : 1501812115281754,
                                                         'status'              : 'open',
                                                         'entryOrder'          : {
                                                             'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4},
                                                         'orderType'           : 'STP',
                                                         'targetPrice'         : 'NONE',
                                                         'instrument'          : 'BTCUSD7Q04',
                                                         'oco'                 : 'e4033320-78b8-11e7-93eb-6c3e3294535e',
                                                         'maxStop'             : 2729.2,
                                                         'entryPrice'          : 2781.5,
                                                         'entryAmount'         : 14380728,
                                                         'commission'          : 0.0005,
                                                         'reward'              : 0,
                                                         'cushion'             : 5,
                                                         'reservedTicks'       : 2,
                                                         'crossMargin'         : False,
                                                         'normalizedEntryPrice': 3595182,
                                                         'normalizedMaxStop'   : 3664077},
                'e4033320-78b8-11e7-93eb-6c3e3294535e': {'uuid'                : 'e4033320-78b8-11e7-93eb-6c3e3294535e',
                                                         'userid'              : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                         'side'                : 'sell',
                                                         'quantity'            : 4,
                                                         'filled'              : 0,
                                                         'cancelled'           : 0,
                                                         'price'               : 'NONE',
                                                         'normalizedPrice'     : 'NONE',
                                                         'averagePrice'        : 0,
                                                         'entryTime'           : 1501812115282178,
                                                         'eventTime'           : 1501812115282178,
                                                         'status'              : 'open',
                                                         'entryOrder'          : {
                                                             'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4},
                                                         'orderType'           : 'TGT',
                                                         'targetPrice'         : 'NONE',
                                                         'instrument'          : 'BTCUSD7Q04',
                                                         'oco'                 : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                                         'entryPrice'          : 2781.5,
                                                         'entryAmount'         : 14380728,
                                                         'commission'          : 0.0005,
                                                         'reward'              : 0,
                                                         'cushion'             : 5,
                                                         'reservedTicks'       : 2,
                                                         'crossMargin'         : False,
                                                         'normalizedEntryPrice': 3595182}},
                'BCHBTC7Q11'       : {}, 'BCHBTC7Q04': {}, 'BTCUSD7Q11': {}, 'MBTCUSD7Q040205': {},
                'MBTCUSD7Q040210'  : {}}, 'positions': {
                'BTCUSD7Q04': {'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'instrument': 'BTCUSD7Q04',
                               'averagePrice': 2781.5, 'quantity': 4, 'entryAmount': -14380728, 'commission': 0}},
            'pnl': {'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'accountid': '2NGJqK6fXWfMMtJwWHdKT59WzqKDxFKagJp',
                    'pnl'   : -7190, 'commission': 7190}, 'margin': 62802579, 'displayMargin': 62802579,
            'accountMargin': 63092539, 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}
        split = {'result'   : [{'op'        : 'split',
                                'response'  : [
                                    {'uuid'                : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                     'userid'              : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell',
                                     'quantity'            : 4, 'filled': 0, 'cancelled': 2, 'price': 2734.2,
                                     'normalizedPrice'     : 3657377, 'averagePrice': 0, 'entryTime': 1501812115281754,
                                     'eventTime'           : 1501812115281754, 'status': 'open',
                                     'entryOrder'          : {'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4},
                                     'orderType'           : 'STP', 'targetPrice': 'NONE', 'instrument': 'BTCUSD7Q04',
                                     'oco'                 : 'e4033320-78b8-11e7-93eb-6c3e3294535e', 'maxStop': 2729.2,
                                     'entryPrice'          : 2781.6, 'entryAmount': 7190364, 'commission': 0.0005,
                                     'reward'              : 0, 'cushion': 5, 'reservedTicks': 2, 'crossMargin': False,
                                     'normalizedEntryPrice': 3595053, 'normalizedMaxStop': 3664077},
                                    {'uuid'                                                    : 'e4033320-78b8-11e7-93eb-6c3e3294535e',
                                     'userid'                                                  : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                     'side'                                                    : 'sell', 'quantity': 4,
                                     'filled'                                                  : 0, 'cancelled': 2,
                                     'price'                                                   : 'NONE',
                                     'normalizedPrice'                                         : 'NONE',
                                     'averagePrice'                                            : 0,
                                     'entryTime'                                               : 1501812115282178,
                                     'eventTime'                                               : 1501812115282178,
                                     'status'                                                  : 'open', 'entryOrder': {
                                        'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'TGT',
                                     'targetPrice'                                             : 'NONE',
                                     'instrument'                                              : 'BTCUSD7Q04',
                                     'oco'                                                     : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                     'entryPrice'                                              : 2781.6,
                                     'entryAmount'                                             : 7190364,
                                     'commission'                                              : 0.0005, 'reward': 0,
                                     'cushion'                                                 : 5, 'reservedTicks': 2,
                                     'crossMargin'                                             : False,
                                     'normalizedEntryPrice'                                    : 3595053},
                                    {'uuid'                : '191d6850-78b9-11e7-9dd3-61812a98a093',
                                     'userid'              : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell',
                                     'quantity'            : 2, 'filled': 0, 'cancelled': 0, 'price': 2734.2,
                                     'normalizedPrice'     : 3657377, 'averagePrice': 0, 'entryTime': 1501812115281754,
                                     'eventTime'           : 1501812115281754, 'status': 'open',
                                     'entryOrder'          : {'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4},
                                     'orderType'           : 'STP', 'targetPrice': 'NONE', 'instrument': 'BTCUSD7Q04',
                                     'oco'                 : '191d6852-78b9-11e7-8e44-382dd3d2e480', 'maxStop': 2729.2,
                                     'entryPrice'          : 2781.6, 'entryAmount': 7190364, 'commission': 0.0005,
                                     'reward'              : 0, 'cushion': 5, 'reservedTicks': 2, 'crossMargin': False,
                                     'normalizedEntryPrice': 3595053, 'normalizedMaxStop': 3664077},
                                    {'uuid'                                                    : '191d6852-78b9-11e7-8e44-382dd3d2e480',
                                     'userid'                                                  : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                     'side'                                                    : 'sell', 'quantity': 2,
                                     'filled'                                                  : 0, 'cancelled': 0,
                                     'price'                                                   : 'NONE',
                                     'normalizedPrice'                                         : 'NONE',
                                     'averagePrice'                                            : 0,
                                     'entryTime'                                               : 1501812115282178,
                                     'eventTime'                                               : 1501812115282178,
                                     'status'                                                  : 'open', 'entryOrder': {
                                        'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'TGT',
                                     'targetPrice'                                             : 'NONE',
                                     'instrument'                                              : 'BTCUSD7Q04',
                                     'oco'                                                     : '191d6850-78b9-11e7-9dd3-61812a98a093',
                                     'entryPrice'                                              : 2781.6,
                                     'entryAmount'                                             : 7190364,
                                     'commission'                                              : 0.0005, 'reward': 0,
                                     'cushion'                                                 : 5, 'reservedTicks': 2,
                                     'crossMargin'                                             : False,
                                     'normalizedEntryPrice'                                    : 3595053}],
                                'statusCode': 200}],
                 'requestid': 'bb762203-a0f9-4392-a36f-73374771af26'}
        bot.on_order_patch(split)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['e4030c10-78b8-11e7-b7bb-1404f32a4ed5'],
                          split['result'][0]['response'][0])
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['e4033320-78b8-11e7-93eb-6c3e3294535e'],
                          split['result'][0]['response'][1])
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['191d6850-78b9-11e7-9dd3-61812a98a093'],
                          split['result'][0]['response'][2])
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['191d6852-78b9-11e7-8e44-382dd3d2e480'],
                          split['result'][0]['response'][3])

    def test_on_patch_merge(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q04': {
            'e4030c10-78b8-11e7-b7bb-1404f32a4ed5': {'uuid'                                                     : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                                     'userid'                                                   : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'                                                     : 'sell',
                                                     'quantity'                                                 : 4,
                                                     'filled'                                                   : 0,
                                                     'cancelled'                                                : 2,
                                                     'price'                                                    : 2734.2,
                                                     'normalizedPrice'                                          : 3657377,
                                                     'averagePrice'                                             : 0,
                                                     'entryTime'                                                : 1501812115281754,
                                                     'eventTime'                                                : 1501812115281754,
                                                     'status'                                                   : 'open',
                                                     'entryOrder'                                               : {
                                                         'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'STP',
                                                     'targetPrice'                                              : 'NONE',
                                                     'instrument'                                               : 'BTCUSD7Q04',
                                                     'oco'                                                      : 'e4033320-78b8-11e7-93eb-6c3e3294535e',
                                                     'maxStop'                                                  : 2729.2,
                                                     'entryPrice'                                               : 2781.6,
                                                     'entryAmount'                                              : 7190364,
                                                     'commission'                                               : 0.0005,
                                                     'reward'                                                   : 0,
                                                     'cushion'                                                  : 5,
                                                     'reservedTicks'                                            : 2,
                                                     'crossMargin'                                              : False,
                                                     'normalizedEntryPrice'                                     : 3595053,
                                                     'normalizedMaxStop'                                        : 3664077},
            'e4033320-78b8-11e7-93eb-6c3e3294535e': {'uuid'                                                     : 'e4033320-78b8-11e7-93eb-6c3e3294535e',
                                                     'userid'                                                   : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'                                                     : 'sell',
                                                     'quantity'                                                 : 4,
                                                     'filled'                                                   : 0,
                                                     'cancelled'                                                : 2,
                                                     'price'                                                    : 'NONE',
                                                     'normalizedPrice'                                          : 'NONE',
                                                     'averagePrice'                                             : 0,
                                                     'entryTime'                                                : 1501812115282178,
                                                     'eventTime'                                                : 1501812115282178,
                                                     'status'                                                   : 'open',
                                                     'entryOrder'                                               : {
                                                         'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'TGT',
                                                     'targetPrice'                                              : 'NONE',
                                                     'instrument'                                               : 'BTCUSD7Q04',
                                                     'oco'                                                      : 'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                                     'entryPrice'                                               : 2781.6,
                                                     'entryAmount'                                              : 7190364,
                                                     'commission'                                               : 0.0005,
                                                     'reward'                                                   : 0,
                                                     'cushion'                                                  : 5,
                                                     'reservedTicks'                                            : 2,
                                                     'crossMargin'                                              : False,
                                                     'normalizedEntryPrice'                                     : 3595053},
            '191d6850-78b9-11e7-9dd3-61812a98a093': {'uuid'                                                     : '191d6850-78b9-11e7-9dd3-61812a98a093',
                                                     'userid'                                                   : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'                                                     : 'sell',
                                                     'quantity'                                                 : 2,
                                                     'filled'                                                   : 0,
                                                     'cancelled'                                                : 0,
                                                     'price'                                                    : 2734.2,
                                                     'normalizedPrice'                                          : 3657377,
                                                     'averagePrice'                                             : 0,
                                                     'entryTime'                                                : 1501812115281754,
                                                     'eventTime'                                                : 1501812115281754,
                                                     'status'                                                   : 'open',
                                                     'entryOrder'                                               : {
                                                         'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'STP',
                                                     'targetPrice'                                              : 'NONE',
                                                     'instrument'                                               : 'BTCUSD7Q04',
                                                     'oco'                                                      : '191d6852-78b9-11e7-8e44-382dd3d2e480',
                                                     'maxStop'                                                  : 2729.2,
                                                     'entryPrice'                                               : 2781.6,
                                                     'entryAmount'                                              : 7190364,
                                                     'commission'                                               : 0.0005,
                                                     'reward'                                                   : 0,
                                                     'cushion'                                                  : 5,
                                                     'reservedTicks'                                            : 2,
                                                     'crossMargin'                                              : False,
                                                     'normalizedEntryPrice'                                     : 3595053,
                                                     'normalizedMaxStop'                                        : 3664077},
            '191d6852-78b9-11e7-8e44-382dd3d2e480': {'uuid'                                                     : '191d6852-78b9-11e7-8e44-382dd3d2e480',
                                                     'userid'                                                   : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                                     'side'                                                     : 'sell',
                                                     'quantity'                                                 : 2,
                                                     'filled'                                                   : 0,
                                                     'cancelled'                                                : 0,
                                                     'price'                                                    : 'NONE',
                                                     'normalizedPrice'                                          : 'NONE',
                                                     'averagePrice'                                             : 0,
                                                     'entryTime'                                                : 1501812115282178,
                                                     'eventTime'                                                : 1501812115282178,
                                                     'status'                                                   : 'open',
                                                     'entryOrder'                                               : {
                                                         'e3f79a60-78b8-11e7-abc5-a2365cd0ffa3': 4}, 'orderType': 'TGT',
                                                     'targetPrice'                                              : 'NONE',
                                                     'instrument'                                               : 'BTCUSD7Q04',
                                                     'oco'                                                      : '191d6850-78b9-11e7-9dd3-61812a98a093',
                                                     'entryPrice'                                               : 2781.6,
                                                     'entryAmount'                                              : 7190364,
                                                     'commission'                                               : 0.0005,
                                                     'reward'                                                   : 0,
                                                     'cushion'                                                  : 5,
                                                     'reservedTicks'                                            : 2,
                                                     'crossMargin'                                              : False,
                                                     'normalizedEntryPrice'                                     : 3595053}},
            'BCHBTC7Q11'                                   : {}, 'BCHBTC7Q04': {}, 'BTCUSD7Q11': {},
            'MBTCUSD7Q040335'                              : {}, 'MBTCUSD7Q040340': {}}, 'positions': {
            'BTCUSD7Q04': {'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'instrument': 'BTCUSD7Q04',
                           'averagePrice': 2781.5, 'quantity': 4, 'entryAmount': -14380728, 'commission': 0}},
            'pnl': {'userid'    : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                    'accountid' : '2NGJqK6fXWfMMtJwWHdKT59WzqKDxFKagJp', 'pnl': -7190,
                    'commission': 7190}, 'margin': 62802579, 'displayMargin': 62802579,
            'accountMargin': 63092539, 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        merge = {'result'   : [{'op'        : 'merge',
                                'response'  : {'added': [
                                    {'uuid'                : 'd80fbd10-78c5-11e7-ad45-eaddc760377a',
                                     'userid'              : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell',
                                     'quantity'            : 4, 'filled': 0, 'cancelled': 0, 'price': 2734.3,
                                     'normalizedPrice'     : 3657243, 'averagePrice': 0, 'entryTime': 1501817678689940,
                                     'eventTime'           : 1501817678689940, 'status': 'open', 'entryOrder': {},
                                     'orderType'           : 'STP', 'targetPrice': 3, 'instrument': 'BTCUSD7Q04',
                                     'oco'                 : 'd810a770-78c5-11e7-b476-8b19e88788c3', 'maxStop': 2729.3,
                                     'executionPrice'      : 0, 'entryPrice': 2781.6, 'entryAmount': 14380728,
                                     'commission'          : None, 'reward': None, 'crossMargin': False,
                                     'normalizedEntryPrice': 3595053, 'normalizedMaxStop': 3663943},
                                    {'uuid'           : 'd810a770-78c5-11e7-b476-8b19e88788c3',
                                     'userid'         : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell',
                                     'quantity'       : 4, 'filled': 0, 'cancelled': 0, 'price': 'NONE',
                                     'normalizedPrice': 'NONE', 'averagePrice': 0, 'entryTime': 1501817678695038,
                                     'eventTime'      : 1501817678695038, 'status': 'open', 'entryOrder': {},
                                     'orderType'      : 'TGT', 'targetPrice': 3, 'instrument': 'BTCUSD7Q04',
                                     'oco'            : 'd80fbd10-78c5-11e7-ad45-eaddc760377a', 'executionPrice': 0,
                                     'entryPrice'     : 2781.6, 'entryAmount': 14380728, 'commission': None,
                                     'reward'         : None, 'crossMargin': False, 'normalizedEntryPrice': 3595053}],
                                    'removed'         : [
                                        '191d6850-78b9-11e7-9dd3-61812a98a093',
                                        '191d6852-78b9-11e7-8e44-382dd3d2e480',
                                        'e4030c10-78b8-11e7-b7bb-1404f32a4ed5',
                                        'e4033320-78b8-11e7-93eb-6c3e3294535e']},
                                'statusCode': 200}],
                 'requestid': 'a44c438d-3cf9-4b9e-8c30-233188411182'}

        bot.on_order_patch(merge)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['d80fbd10-78c5-11e7-ad45-eaddc760377a'],
                          merge['result'][0]['response']['added'][0])
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['d810a770-78c5-11e7-b476-8b19e88788c3'],
                          merge['result'][0]['response']['added'][1])
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['191d6850-78b9-11e7-9dd3-61812a98a093'],
                          None)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['191d6852-78b9-11e7-8e44-382dd3d2e480'],
                          None)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['e4030c10-78b8-11e7-b7bb-1404f32a4ed5'],
                          None)
        self.assertEquals(bot.coinpit_user_details['orders']['BTCUSD7Q04']['e4033320-78b8-11e7-93eb-6c3e3294535e'],
                          None)

    def test_get_price_for(self):
        bot = mmbot.MMBot()
        tupples = [[2877.2, 28491], [2876.8, 56982], [2860.9, 100], [2853.5, 142455], [2841, 50], [2840.5, 284909],
                   [2840.4, 2000], [2832.5, 200], [2823.2, 200], [2823, 10]]
        quantity = 100000
        price = bot.get_price_for(quantity, tupples)
        self.assertEquals(price, 2853.5)
        pass

    def test_get_coinpit_instrument(self):
        bot = mmbot.MMBot()
        bot.coinpit_config = {"alias": {"MBTCUSDT": "MBTCUSD7Q051810",
                                        "BTCUSDF" : "BTCUSD7Q18",
                                        "MBTCUSDF": "MBTCUSD7Q051805",
                                        "BCHBTCW" : "BCHBTC7Q11",
                                        "BTCUSDW" : "BTCUSD7Q11",
                                        "BCHBTCF" : "BCHBTC7Q18"}}
        orig_symbol = settings.COINPIT_SYMBOL
        settings.COINPIT_SYMBOL = 'BTCUSDW'
        symbol = bot.get_coinpit_instrument()
        self.assertEquals(symbol, 'BTCUSD7Q11')

        settings.COINPIT_SYMBOL = orig_symbol

    def test_get_current_bid_ask(self):
        bot = mmbot.MMBot()
        bot.coinpit_user_details = {'orders': {'BTCUSD7Q18'                : {}, 'BCHBTC7Q11': {}, 'BTCUSD7Q11': {
            '9795aa50-7a06-11e7-b1fa-ea149550e9ca': {
                'uuid'        : '9795aa50-7a06-11e7-b1fa-ea149550e9ca',
                'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell', 'quantity': 4,
                'filled'      : 0, 'cancelled': 0, 'price': 3275.8, 'normalizedPrice': 3052689,
                'averagePrice': 0, 'entryTime': 1501955438965755, 'eventTime': 1501955438965755,
                'status'      : 'open', 'entryOrder': {'9789c370-7a06-11e7-b624-6281d4d4e9c6': 4},
                'orderType'   : 'STP', 'targetPrice': 'NONE', 'instrument': 'BTCUSD7Q11',
                'oco'         : '9795d160-7a06-11e7-adeb-4d00d57348bf', 'maxStop': 3270.8, 'entryPrice': 3333.8,
                'entryAmount' : 11998320, 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
                'crossMargin' : False, 'normalizedEntryPrice': 2999580, 'normalizedMaxStop': 3057356},
            '9795d160-7a06-11e7-adeb-4d00d57348bf': {
                'uuid'         : '9795d160-7a06-11e7-adeb-4d00d57348bf',
                'userid'       : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell', 'quantity': 4, 'filled': 0,
                'cancelled'    : 0, 'price': 'NONE', 'normalizedPrice': 'NONE', 'averagePrice': 0,
                'entryTime'    : 1501955438966394, 'eventTime': 1501955438966394, 'status': 'open',
                'entryOrder'   : {'9789c370-7a06-11e7-b624-6281d4d4e9c6': 4}, 'orderType': 'TGT',
                'targetPrice'  : 'NONE', 'instrument': 'BTCUSD7Q11', 'oco': '9795aa50-7a06-11e7-b1fa-ea149550e9ca',
                'entryPrice'   : 3333.8, 'entryAmount': 11998320, 'commission': 0.0005, 'reward': 0, 'cushion': 5,
                'reservedTicks': 2, 'crossMargin': False, 'normalizedEntryPrice': 2999580},
            '98cfff10-7a06-11e7-a3f9-50e3b2a156fc': {
                'uuid'        : '98cfff10-7a06-11e7-a3f9-50e3b2a156fc',
                'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell', 'quantity': 4,
                'filled'      : 0, 'cancelled': 0, 'price': 3278.3, 'normalizedPrice': 3050361,
                'averagePrice': 0, 'entryTime': 1501955441025522, 'eventTime': 1501955441025522,
                'status'      : 'open', 'entryOrder': {'98c68930-7a06-11e7-852a-2ac2de074234': 4},
                'orderType'   : 'STP', 'targetPrice': 'NONE', 'instrument': 'BTCUSD7Q11',
                'oco'         : '98cfff11-7a06-11e7-b900-e084ce63c92d', 'maxStop': 3273.3, 'entryPrice': 3336.3,
                'entryAmount' : 11989328, 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
                'crossMargin' : False, 'normalizedEntryPrice': 2997332, 'normalizedMaxStop': 3055021},
            '98cfff11-7a06-11e7-b900-e084ce63c92d': {
                'uuid'         : '98cfff11-7a06-11e7-b900-e084ce63c92d',
                'userid'       : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell', 'quantity': 4, 'filled': 0,
                'cancelled'    : 0, 'price': 'NONE', 'normalizedPrice': 'NONE', 'averagePrice': 0,
                'entryTime'    : 1501955441025867, 'eventTime': 1501955441025867, 'status': 'open',
                'entryOrder'   : {'98c68930-7a06-11e7-852a-2ac2de074234': 4}, 'orderType': 'TGT',
                'targetPrice'  : 'NONE', 'instrument': 'BTCUSD7Q11', 'oco': '98cfff10-7a06-11e7-a3f9-50e3b2a156fc',
                'entryPrice'   : 3336.3, 'entryAmount': 11989328, 'commission': 0.0005, 'reward': 0, 'cushion': 5,
                'reservedTicks': 2, 'crossMargin': False, 'normalizedEntryPrice': 2997332},
            '9a2a8600-7a06-11e7-bdb7-9e0e10d476a3': {
                'uuid'       : '9a2a8600-7a06-11e7-bdb7-9e0e10d476a3',
                'userid'     : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'buy', 'quantity': 4, 'filled': 0,
                'cancelled'  : 0, 'price': 3223.6, 'normalizedPrice': 3102122, 'averagePrice': 0,
                'entryTime'  : 1501955443296456, 'eventTime': 1501955443296456, 'status': 'open', 'entryOrder': {},
                'orderType'  : 'LMT', 'targetPrice': 'NONE', 'clientid': '0fef672c-c97f-46fb-8ac5-af1422d4ed37',
                'instrument' : 'BTCUSD7Q11', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
                'crossMargin': False, 'marginPerQty': 60770},
            '9ae71f40-7a06-11e7-acdd-ac5b6c085f2d': {
                'uuid'       : '9ae71f40-7a06-11e7-acdd-ac5b6c085f2d',
                'userid'     : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'side': 'sell', 'quantity': 4, 'filled': 0,
                'cancelled'  : 0, 'price': 3364.9, 'normalizedPrice': 2971857, 'averagePrice': 0,
                'entryTime'  : 1501955444532642, 'eventTime': 1501955444532642, 'status': 'open', 'entryOrder': {},
                'orderType'  : 'LMT', 'targetPrice': 'NONE', 'clientid': 'fcf27cb1-d0ee-418a-83c0-05f73012e012',
                'instrument' : 'BTCUSD7Q11', 'commission': 0.0005, 'reward': 0, 'cushion': 5, 'reservedTicks': 2,
                'crossMargin': False, 'marginPerQty': 60770}}, 'BCHBTC7Q18': {}, 'MBTCUSD7Q051755': {},
                                               'MBTCUSD7Q051800'           : {}}, 'positions': {
            'BTCUSD7Q11': {'userid'      : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU', 'instrument': 'BTCUSD7Q11',
                           'averagePrice': 3335, 'quantity': 8, 'entryAmount': -23987648, 'commission': 0}},
                                    'pnl': {'userid'    : 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU',
                                            'accountid' : '2NGJqK6fXWfMMtJwWHdKT59WzqKDxFKagJp', 'pnl': -11994,
                                            'commission': 11994}, 'margin': 62427127, 'displayMargin': 62427127,
                                    'accountMargin': 63399135, 'userid': 'moVB8e8oWX1oKjaaesdimAGqJHxjih8kjU'}

        bot.coinpit_config = {"alias": {"MBTCUSDT": "MBTCUSD7Q051810",
                                        "BTCUSDF" : "BTCUSD7Q18",
                                        "MBTCUSDF": "MBTCUSD7Q051805",
                                        "BCHBTCW" : "BCHBTC7Q11",
                                        "BTCUSDW" : "BTCUSD7Q11",
                                        "BCHBTCF" : "BCHBTC7Q18"}}

        orders = bot.get_current_bid_ask()
        result = {'bids': [bot.coinpit_user_details['orders']['BTCUSD7Q11']['9a2a8600-7a06-11e7-bdb7-9e0e10d476a3']],
                  'asks': [bot.coinpit_user_details['orders']['BTCUSD7Q11']['9ae71f40-7a06-11e7-acdd-ac5b6c085f2d']]
                  }
        self.assertEquals(result, orders)

    def test_get_available_qty(self):
        bot = mmbot.MMBot()
        orders = [
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a3', 'quantity': 40, 'filled': 0, 'cancelled': 2},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a4', 'quantity': 40, 'filled': 1, 'cancelled': 3},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a5', 'quantity': 40, 'filled': 2, 'cancelled': 5},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a6', 'quantity': 40, 'filled': 3, 'cancelled': 6},
        ]
        available = bot.get_available_qty(orders)
        self.assertEquals(available, 138)

    def test_get_patch_request_for_coinpit(self):
        bot = mmbot.MMBot()
        orders = [
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a3', 'quantity': 10, 'filled': 0, 'cancelled': 2},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a4', 'quantity': 10, 'filled': 1, 'cancelled': 3},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a5', 'quantity': 10, 'filled': 2, 'cancelled': 5},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a6', 'quantity': 10, 'filled': 3, 'cancelled': 6},
        ]

        expected_updates = [
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a3', 'price': 3200.0},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a4', 'price': 3200.0},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a5', 'price': 3200.0},
            {'uuid': '9a2a8600-7a06-11e7-bdb7-9e0e10d476a6', 'price': 3200.0}
        ]

        expected_adds = [
            {
                "instrument" : settings.COINPIT_SYMBOL,
                "side"       : "buy",
                "quantity"   : settings.COINPIT_QTY - 18,
                "price"      : 3200.0,
                "orderType"  : "LMT",
                "crossMargin": True,
                "targetPrice": "NONE"
            }
        ]
        updates = []
        adds = []
        bot.populate_replace_add_for_coinpit('buy', 3200.0, orders, updates, adds)
        self.assertEquals(updates, expected_updates)
        self.assertEquals(adds, expected_adds)

    def test_on_price_band(self):
        bot = mmbot.MMBot()
        bot.coinpit_config = {"alias": {"MBTCUSDT": "MBTCUSD7Q051810",
                                        "BTCUSDF" : "BTCUSD7Q18",
                                        "MBTCUSDF": "MBTCUSD7Q051805",
                                        "BCHBTCW" : "BCHBTC7Q11",
                                        "BTCUSDW" : "BTCUSD7Q11",
                                        "BCHBTCF" : "BCHBTC7Q18"}}
        data = {
            'BTCUSD7Q18'     : {'price': 3218.4, 'instrument': 'BTCUSD7Q18'},
            'BTCUSD7Q11'     : {'price': 3218.4, 'instrument': 'BTCUSD7Q11'},
            'MBTCUSD7Q060350': {'price': 3218.4, 'instrument': 'MBTCUSD7Q060350'},
            'MBTCUSD7Q060355': {'price': 3218.4, 'instrument': 'MBTCUSD7Q060355'}
        }
        bot.current_index = None
        bot.on_price_band(data)
        self.assertEquals(bot.current_index, data['BTCUSD7Q11']['price'])

    @freeze_time("2017-08-05 08:07:29.511")
    def test_get_current_premium(self):
        bot = mmbot.MMBot()
        bot.coinpit_config = bot.coinpit_config = {
            "instruments": {
                "BTCUSD7Q11": {"type"                  : "inverse", "template": "BTCUSD", "commission": 0.0005,
                               "reward"                : 0,
                               "stopcushion"           : 5, "stopprice": 2, "targetprice": 3,
                               "crossMarginInitialStop": 50,
                               "ticksize"              : 1, "ticksperpoint": 10, "contractusdvalue": 100,
                               "bandUpperLimit"        : 0.01, "bandLowerLimit": 0.01, "introducerReward": 0,
                               "introducedReward"      : 0, "rewardsCalculationInterval": 14400,
                               "minMarketStop"         : 1.6,
                               "minLimitStop"          : 1.6, "uplDecimalPlaces": 8,
                               "externalFeed"          : "coinpit-index#BTCUSD",
                               "expiryClass"           : "weekly", "maxLeverage": 100, "symbol": "BTCUSD7Q11",
                               "start"                 : 1501262100000, "expiry": 1502471700000,
                               "next"                  : "BTCUSD7Q18",
                               "status"                : "active"},
            },
            "alias"      : {"BTCUSDF" : "BTCUSD7Q18",
                            "MBTCUSDF": "MBTCUSD7Q060350",
                            "MBTCUSDT": "MBTCUSD7Q060355",
                            "BTCUSDW" : "BTCUSD7Q11"}
        }

        orig_rate = settings.INTEREST_RATE
        settings.INTEREST_RATE = 0.06
        bot.current_index = 3000
        premium = bot.get_current_premium()
        self.assertEquals(premium, 3.5)
        settings.INTEREST_RATE = orig_rate
