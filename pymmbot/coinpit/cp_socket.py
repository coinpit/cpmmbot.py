import _thread
from urllib.parse import urlparse

from socketIO_client import SocketIO

from pymmbot.coinpit import crypto
from pymmbot.utils import common_util


class CP_Socket(object):
    def __init__(self):
        self.coinpit_socket = None
        self.account = None

    def connect(self, url, account=None):
        assert (url is not None), "provide server url"
        parsed_url = urlparse(url)
        host = ('https://' if parsed_url.scheme == 'https' else '') + parsed_url.hostname
        port = parsed_url.port
        self.coinpit_socket = SocketIO(host, port)
        _thread.start_new_thread(self.coinpit_socket.wait, ())
        self.account = account
        self.register()

    @staticmethod
    def get_headers(userid, name, secret, method, uri, body=None):
        nonce = common_util.current_milli_time()
        auth = crypto.get_auth(userid, name, secret, str(nonce), method, uri, body)
        return {'Authorization': auth, 'Nonce': nonce}

    def send(self, request):
        assert (self.account is not None), "account is not set. call cp_socket.connect(url, account) method"
        method = request['method']
        uri = request['uri']
        body = request['body']
        headers = self.get_headers(self.account.userid, self.account.name, self.account.secretKey, method, uri, body)
        data = {"headers": headers, "method": method, "uri": uri, "body": body}
        self.coinpit_socket.emit(method + " " + uri, data)

    def register(self):
        if self.account is None:
            print("account is not set. call cp_socket.connect(url, account) method")
            return
        self.send({"method": "GET", "uri": "/register",
                   "body"  : {"userid": self.account.userid, "publicKey": self.account.publicKey}})

    def unregister(self):
        if self.account is None:
            print("account is not set. call cp_socket.connect(url, account) method")
            return
        self.send({"method": "GET", "uri": "/unregister",
                   "body"  : {"userid": self.account.userid, "publicKey": self.account.publicKey}})

    def subscribe(self, event_map):
        assert (self.coinpit_socket is not None), "call cp_socket.connect(url, account) to create socket connection"
        for event in event_map:
            print('event', event)
            self.coinpit_socket.on(event, event_map[event])
