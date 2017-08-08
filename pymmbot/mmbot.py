import json
import logging
from pymmbot.bitmex import bm_socket, bitmex
from pymmbot.coinpit import account, cp_socket, rest
from settings import settings
from easydict import EasyDict as edict
from pymmbot.utils import common_util
import math
import traceback
import sys


# import logging.config
# from os import path


class MMBot(object):
    def __init__(self):
        # log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
        # logging.config.fileConfig(log_file_path)
        # self.log = logging.getLogger('root')
        self.bitmex = None
        self.current_spread = None
        self.current_price = {'buy': None, 'sell': None}
        self.current_index = None
        self.coinpit_account = None
        self.coinpit_socket = None
        self.coinpit_rest = None
        self.coinpit_user_details = None
        self.coinpit_position = None
        self.coinpit_config = {'config': None, 'instruments': None, 'alias': None}
        self.orders = None
        self.read_only = False
        self.bitmex_socket = None

    def connect_coinpit(self):
        # assert (apikey is not None), 'apikey is missing.'
        # assert (url is not None), "provide server url"
        url = settings.COINPIT_URL
        apikey = settings.COINPIT_API_KEY
        self.coinpit_account = account.Account(apikey)
        self.coinpit_rest = rest.Rest(url, self.coinpit_account)
        self.get_account_details()
        self.coinpit_socket = cp_socket.CP_Socket()
        self.coinpit_socket.connect(url, self.coinpit_account)
        self.subscribe()

    def connect_bitmex(self):
        self.bitmex = bitmex.Bitmex()
        self.bitmex_socket = bm_socket.BM_Socket()
        self.bitmex_socket.connect(edict({
            'orderBook10': self.on_bitmex_orderbook_change,
            'position'   : self.on_bitmex_position
        }))

    def get_account_details(self):
        response = self.coinpit_rest.get("/all/config")
        self.coinpit_config = json.loads(response.text)
        print('coinpit_config', response.text)
        response = self.coinpit_rest.get("/account")
        self.coinpit_user_details = json.loads(response.text)
        self.replenish_coinpit_limit_orders()

    def on_config(self, data):
        self.coinpit_config['config'] = data

    def on_read_only(self, data):
        self.read_only = data['readonly']
        print('on_read_only', data)

    def on_connect(self, data=None):
        print('on_connect', data)

    def on_disconnect(self, data=None):
        print('on_disconnect', data)

    def on_order_add(self, data):
        print('on order add', data)
        self.add_orders_to_cache(data['result'])

    def on_order_del(self, data):
        print('on_order_del', data)
        self.del_orders_to_cache(data['result'])
        self.replenish_coinpit_limit_orders()

    def on_order_error(self, data):
        print('on_order_error', data)

    def on_order_update(self, data):
        print('on_order_update', data)
        orders = data['result']
        self.update_orders_to_cache(orders)

    def on_order_patch(self, data):
        print('on_order_patch', data)
        ops = data['result']
        for op in ops:
            if op['op'] == 'remove':
                self.del_orders_to_cache(op['response'])
                self.replenish_coinpit_limit_orders()
            if op['op'] == 'add':
                self.add_orders_to_cache(op['response'])
            if op['op'] == 'replace':
                self.update_orders_to_cache(op['response'])
            if op['op'] == 'split':
                self.add_orders_to_cache(op['response'])
            if op['op'] == 'merge':
                self.add_orders_to_cache(op['response']['added'])
                self.del_orders_to_cache(op['response']['removed'])

    def on_account(self, data):
        print('on account', data)
        if 'userDetails' in data:
            self.coinpit_user_details = data['userDetails']
            self.replenish_coinpit_limit_orders()
        self.hedge_on_bitmex()

    def on_auth_error(self, data):
        print('on_auth_error', data)

    def on_instruments(self, data):
        self.coinpit_config['instruments'] = data

    def on_alias(self, data):
        self.coinpit_config['alias'] = data

    def subscribe(self):
        event_map = {
            'config'          : self.on_config,
            'readonly'        : self.on_read_only,
            'reconnect'       : self.on_connect,
            'connect_error'   : self.on_disconnect,
            'connect_timeout' : self.on_disconnect,
            'disconnect'      : self.on_disconnect,
            'reconnect_error' : self.on_disconnect,
            'reconnect_failed': self.on_disconnect,
            'order_add'       : self.on_order_add,
            'order_del'       : self.on_order_del,
            'order_error'     : self.on_order_error,
            'order_update'    : self.on_order_update,
            'order_patch'     : self.on_order_patch,
            'account'         : self.on_account,
            'auth_error'      : self.on_auth_error,
            'instruments'     : self.on_instruments,
            'alias'           : self.on_alias,
            'priceband'       : self.on_price_band
        }
        self.coinpit_socket.subscribe(event_map)

    def add_orders_to_cache(self, orders):
        for order in orders:
            if self.coinpit_user_details is None:
                self.coinpit_user_details = {}
            if 'orders' not in self.coinpit_user_details:
                self.coinpit_user_details['orders'] = {}
            if order['instrument'] not in self.coinpit_user_details['orders']:
                self.coinpit_user_details['orders'][order['instrument']] = {}
            self.coinpit_user_details['orders'][order['instrument']][order['uuid']] = order

    def del_orders_to_cache(self, uuids):
        if self.coinpit_user_details is None or 'orders' not in self.coinpit_user_details:
            self.get_account_details()
            return
        for instrument in self.coinpit_user_details['orders']:
            self.remove_order_in_each_instrument(self.coinpit_user_details['orders'][instrument], uuids)

    def update_orders_to_cache(self, orders):
        for order in orders:
            if self.coinpit_user_details is None or \
                            'orders' not in self.coinpit_user_details or \
                            order['instrument'] not in self.coinpit_user_details['orders'] or \
                            order['uuid'] not in self.coinpit_user_details['orders'][order['instrument']]:
                self.get_account_details()
                return
            else:
                self.coinpit_user_details['orders'][order['instrument']][order['uuid']] = order

    def split_orders_to_cache(self, orders):
        self.add_orders_to_cache(orders)

    def replenish_coinpit_limit_orders(self):
        if self.current_index is None or self.current_spread is None: return
        premium = self.get_current_premium()
        buy = round(self.current_index - self.current_spread / 2 + premium, settings.COINPIT_TICK_SIZE)
        sell = round(self.current_index + self.current_spread / 2 + premium, settings.COINPIT_TICK_SIZE)
        self.send_orders_to_coinpit(buy, sell)

    def send_orders_to_coinpit(self, buy_price, sell_price):
        orders = self.get_current_bid_ask()
        updates = []
        adds = []
        self.populate_replace_add_for_coinpit('buy', buy_price, orders['buys'], updates, adds)
        self.populate_replace_add_for_coinpit('sell', sell_price, orders['sells'], updates, adds)
        patch = []
        if len(updates) > 0:
            patch.append({'op': 'replace', 'value': updates})
        if len(adds) > 0:
            patch.append({'op': 'add', 'value': adds})
        if len(patch) > 0:
            self.coinpit_rest.auth_server_call('PATCH', '/order', patch)

    @staticmethod
    def remove_order_in_each_instrument(order_map, uuids):
        if order_map is None:
            return
        for uuid in uuids:
            if uuid in order_map:
                order_map[uuid] = None

    def get_price_for(self, quantity, tuples):
        total = 0
        price = None
        for tuple in tuples:
            total += tuple[1]
            price = tuple[0]
            if total >= quantity:
                return tuple[0]
        return price

    def get_current_bid_ask(self):
        orders = {'buys': [], 'sells': []}
        instrument = self.get_coinpit_instrument()
        for uuid in self.coinpit_user_details['orders'][instrument]:
            order = self.coinpit_user_details['orders'][instrument][uuid]
            if order is not None and order['orderType'] == 'LMT':
                side = orders['buys'] if order['side'] == 'buy' else orders['sells']
                side.insert(0, order)
        return orders

    def populate_replace_add_for_coinpit(self, side, price, orders, replace, add):
        if price is None: return
        total = settings.COINPIT_QTY
        available = self.get_available_qty(orders)
        if self.current_price[side] != price:
            self.current_price[side] = price
            for order in orders:
                replace.append({'uuid': order['uuid'], 'price': price})
        new_qty = total - available
        if new_qty > 0:
            add.append({
                "instrument" : settings.COINPIT_SYMBOL,
                "side"       : side,
                "quantity"   : new_qty,
                "price"      : price,
                "orderType"  : "LMT",
                "crossMargin": True,
                "targetPrice": "NONE"
            })

    def on_bitmex_orderbook_change(self, data):
        try:
            if data is None or 'bids' not in data or 'asks' not in data:
                print("Invalid orderbook from bitmex", data)
                return
            buy_price = self.get_price_for(
                settings.COINPIT_QTY * settings.COINPIT_BITMEX_RATIO * settings.QUANTITY_MULTIPLIER,
                data['bids'])
            sell_price = self.get_price_for(
                settings.COINPIT_QTY * settings.COINPIT_BITMEX_RATIO * settings.QUANTITY_MULTIPLIER,
                data['asks'])
            self.current_spread = round(sell_price - buy_price, settings.COINPIT_TICK_SIZE)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

        self.replenish_coinpit_limit_orders()

    def on_bitmex_position(self, data):
        print('bitmex position', self.bitmex_socket.position())
        # self.hedge_on_bitmex()

    # premium = current_index * interest_rate * days_left /365
    def get_current_premium(self):
        symbol = self.get_coinpit_instrument()
        instrument = self.coinpit_config['instruments'][symbol]
        expiry = instrument['expiry']
        current = common_util.current_milli_time()
        diff = expiry - current
        days = math.ceil(diff / (24 * 60 * 60 * 1000))
        premium = self.current_index * settings.INTEREST_RATE * days / 365
        return round(premium, settings.COINPIT_TICK_SIZE)

    def on_price_band(self, data):
        print('on_price_band', data)
        self.current_index = data[self.get_coinpit_instrument()]['price']
        self.replenish_coinpit_limit_orders()

    def hedge_on_bitmex(self):
        if self.coinpit_user_details is None: return
        if len(self.bitmex_socket.orders()) > 0: self.bitmex.cancel_all_orders()
        positions = self.coinpit_user_details['positions']
        instrument = self.get_coinpit_instrument()
        position = None if instrument not in positions else positions[instrument]
        on_coinpit = 0 if position is None else position['quantity']
        on_bitmex = self.get_total_position_in_bitmex()
        hedge_count = on_bitmex + on_coinpit * settings.COINPIT_BITMEX_RATIO
        if hedge_count == 0: return
        side = 'Sell' if hedge_count > 0 else 'Buy'
        if self.bitmex: self.bitmex.place_order(abs(hedge_count), side, settings.BITMEX_TRAILING_PEG)

    def get_total_position_in_bitmex(self):
        position = self.bitmex_socket.position()[0]
        return position['currentQty']

    @staticmethod
    def get_available_qty(orders):
        available = 0
        for order in orders:
            available = available + order['quantity'] - order['filled'] - order['cancelled']
        return available

    def get_coinpit_instrument(self):
        assert (self.coinpit_config is not None and 'alias' in self.coinpit_config), 'coinpit_config not set'
        return self.coinpit_config['alias'][settings.COINPIT_SYMBOL]
