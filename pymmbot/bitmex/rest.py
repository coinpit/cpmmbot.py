import json
from urllib.parse import urlparse

import requests

from pymmbot.coinpit import crypto
from utils import common_util


class Rest(object):
    def __init__(self, base_url, account=None):
        self.base_url = base_url
        parsed_url = urlparse(base_url)
        self.host = parsed_url.hostname
        self.account = account
        self.methods = {
            'GET'    : requests.get,
            'POST'   : requests.post,
            'PUT'    : requests.put,
            'DELETE' : requests.delete,
            'PATCH'  : requests.patch,
            'OPTIONS': requests.options
        }

    def get(self, url):
        if url.startswith("/all/") or url.startswith("/auth/"):
            return self.server_call(url)
        return self.auth_server_call("GET", url)

    def server_call(self, url, headers=None):
        if headers is None:
            headers = {'Accept': 'application/json'}
        try:
            return requests.get(self.base_url + url, headers=headers)
        except Exception as err:
            print("Error on REST call {} \n {}".format(self.base_url + url, err))

    def sparse_json(self, body=None):
        if body is None:
            return None
        result = json.dumps(body, separators=(',', ':'))
        return None if result == '{}' else result

    def auth_server_call(self, method, url, body=None):
        assert self.account is not None, "Call to server requiring auth needs account"
        try:
            sparse_body = self.sparse_json(body)
            headers = self.get_headers(method, url, sparse_body)
            method = self.methods[method]
            return method(url=self.base_url + url, json=body, headers=headers)
        except Exception as err:
            print("Error on REST call {} \n {}".format(self.base_url + url, err))

    def get_headers(self, method, url, body):
        nonce = str(common_util.current_milli_time())
        auth = crypto.get_auth(self.account.userid, self.account.name, self.account.secretKey, nonce, method, url, body)
        return {
            "Authorization": auth,
            "Nonce"        : nonce,
            'Accept'       : 'application/json'
        }
