import logging
import json
from pymmbot.settings import settings
from pymmbot.coinpit import cp_socket, rest


class Coinpit(object):
    def __init__(self):
        self.socket = cp_socket.CP_Socket()
        self.handlers = None
        self.current_index = None
        self.rest = None
        self.user_details = None
        self.position = None
        self.config = {'config': None, 'instruments': None, 'alias': None}
        self.orders = None
        self.read_only = False

    def connect(self, handlers):
        self.handlers = handlers
        self.rest = rest.Rest()
        self.get_account_details()
        self.socket.connect()
        self.subscribe()

    def get_account_details(self):
        response = self.rest.get("/all/config")
        self.config = json.loads(response.text)
        print('coinpit_config', response.text)
        response = self.rest.get("/account")
        self.user_details = json.loads(response.text)
        # self.handlers['account']()

    def on_config(self, data):
        self.config['config'] = data

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
        self.handlers['del']()

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
                self.handlers['del']()
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
            self.user_details = data['userDetails']
        self.handlers['account']()
        # self.replenish_coinpit_limit_orders()
        # self.hedge_on_bitmex()

    def on_auth_error(self, data):
        print('on_auth_error', data)

    def on_instruments(self, data):
        self.config['instruments'] = data

    def on_alias(self, data):
        self.config['alias'] = data

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
        self.socket.subscribe(event_map)

    def add_orders_to_cache(self, orders):
        for order in orders:
            if self.user_details is None:
                self.user_details = {}
            if 'orders' not in self.user_details:
                self.user_details['orders'] = {}
            if order['instrument'] not in self.user_details['orders']:
                self.user_details['orders'][order['instrument']] = {}
            self.user_details['orders'][order['instrument']][order['uuid']] = order

    def del_orders_to_cache(self, uuids):
        if self.user_details is None or 'orders' not in self.user_details:
            self.get_account_details()
            return
        for instrument in self.user_details['orders']:
            self.remove_order_in_each_instrument(self.user_details['orders'][instrument], uuids)

    def update_orders_to_cache(self, orders):
        for order in orders:
            if self.user_details is None or \
                            'orders' not in self.user_details or \
                            order['instrument'] not in self.user_details['orders'] or \
                            order['uuid'] not in self.user_details['orders'][order['instrument']]:
                self.get_account_details()
                return
            else:
                self.user_details['orders'][order['instrument']][order['uuid']] = order

    def split_orders_to_cache(self, orders):
        self.add_orders_to_cache(orders)

    def on_price_band(self, data):
        print('on_price_band', data)
        self.current_index = data[self.get_coinpit_instrument()]['price']
        self.handlers['index']()

    def get_coinpit_instrument(self):
        assert (self.config is not None and 'alias' in self.config), 'coinpit_config not set'
        return self.config['alias'][settings.COINPIT_SYMBOL]

    def index(self):
        return self.current_index
    @staticmethod
    def remove_order_in_each_instrument(order_map, uuids):
        if order_map is None:
            return
        for uuid in uuids:
            if uuid in order_map:
                order_map[uuid] = None
