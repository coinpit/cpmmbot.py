import _thread
import json
import time
import six
from time import sleep
from urllib.parse import urlparse
from nacl.bindings import crypto_sign, crypto_sign_BYTES
from nacl.encoding import Base64Encoder
from socketIO_client import SocketIO

current_milli_time = lambda: int(round(time.time() * 1000))


class MMBot(object):
    def __init__(self, apikey):
        assert (apikey is not None), 'apikey is missing.'
        self.apikey = apikey
        self.coinpit_socket = None
        print('starting bot')

    async def wait_for_coinpit_socket(self):
        await self.coinpit_socket.wait()

    def connect(self, url):
        assert (url is not None), "provide server url"
        parsed_url = urlparse(url)
        print('parsed_url', parsed_url)
        host = ('https://' if parsed_url.scheme == 'https' else '') + parsed_url.hostname
        port = parsed_url.port
        print('host', host, 'port', port)
        self.coinpit_socket = SocketIO(host, port)
        _thread.start_new_thread(self.coinpit_socket.wait, ())

    def get_headers(self, user_id, name, secret, nonce, method, uri, body=None):
        if body is not None:
            if not isinstance(body, six.string_types):
                try:
                    body = json.dumps(body, separators=(',', ':'))
                except ValueError as e:
                    print('invalid body. json or string are valid body type')
        request_string = '{"method":"' + method + '","uri":"' + uri + (
            '",' if (body is None) else '","body":' + body + ',') + '"nonce":"' + nonce + '"}'
        raw_signed = crypto_sign(request_string.encode(), bytes.fromhex(secret))
        signature = Base64Encoder.encode(raw_signed[:crypto_sign_BYTES])
        headers = {
            'Authorization': 'SIGN ' + user_id + "." + name + ':' + signature.decode(),
            'Nonce'        : nonce
        }
        return headers

    def send(self, request):
        method = request['method']
        uri = request['uri']
        body = request['body']
        nonce = str(current_milli_time())
        headers = self.get_headers(self.apikey['userid'], self.apikey['name'], self.apikey['secretKey'],
                                   nonce, method, uri, body)
        data = {"headers": headers, "method": method, "uri": uri, "body": body}
        self.coinpit_socket.emit(method + " " + uri, data)

    def register(self):
        self.send({"method": "GET", "uri": "/register",
                   "body"  : {"userid": self.apikey['userid'], "publicKey": self.apikey["publicKey"]}})

    def unregister(self):
        self.send({"method": "GET", "uri": "/unregister",
                   "body"  : {"userid": self.apikey['userid'], "publicKey": self.apikey["publicKey"]}})

    def on_trade(self, data):
        print('on_trade', data)

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
            'trade'           : self.on_trade,
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

        for event in event_map:
            print('event', event)
            self.coinpit_socket.on(event, event_map[event])

    @staticmethod
    def loop():
        while True:
            sleep(100)

