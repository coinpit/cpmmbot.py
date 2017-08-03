from pymmbot.coinpit import account, cp_socket, rest
import json

class MMBot(object):
    def __init__(self):
        self.coinpit_account = None
        self.coinpit_socket = None
        self.coinpit_rest = None
        self.orders = {"buy": {}, "sell": {}}
        self.position = None

    def connect_coinpit(self, url, apikey):
        assert (apikey is not None), 'apikey is missing.'
        assert (url is not None), "provide server url"
        self.coinpit_account = account.Account(apikey)
        self.coinpit_socket = cp_socket.CP_Socket()
        self.coinpit_socket.connect(url, self.coinpit_account)
        self.subscribe()
        self.coinpit_rest = rest.Rest(url, self.coinpit_account)

    def update_client_cache(self):
        response = self.coinpit_rest.get("/account")
        self.on_account(json.loads(response.text))

    def on_config(self, data):
        print('on_config', data)

    def on_read_only(self, data):
        print('on_read_only', data)

    def on_connect(self, data=None):
        print('on_connect', data)

    def on_disconnect(self, data=None):
        print('on_disconnect', data)

    def on_order_add(self, data):
        print('on_order_add', data)

    def on_order_del(self, data):
        print('on_order_del', data)

    def on_order_error(self, data):
        print('on_order_error', data)

    def on_order_update(self, data):
        print('on_order_update', data)

    def on_order_patch(self, data):
        print('on_order_patch', data)

    def on_account(self, data):
        print('on_account', data)

    def on_auth_error(self, data):
        print('on_auth_error', data)

    def on_instruments(self, data):
        print('on_instruments', data)

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
            'instruments'     : self.on_instruments
        }
        self.coinpit_socket.subscribe(event_map)
