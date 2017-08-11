import base64
import uuid
import requests
import json
import logging
from pymmbot.settings import settings
from pymmbot.bitmex.auth import APIKeyAuthWithExpires
from pymmbot.bitmex import bm_socket
from time import sleep


class Bitmex(object):
    def __init__(self):
        self.orderIDPrefix = 'mm-'
        self.session = requests.Session()
        self.session.headers.update({'user-agent': 'liquidbot-1.0'})
        self.socket = bm_socket.BM_Socket()
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self, handlers):
        self.socket.connect(handlers)

    def cancel_all_orders(self):
        self._curl_bitmex(api='order/all', verb='DELETE')

    def place_order(self, quantity, side, offset):
        """Place an order."""
        endpoint = "order"
        # Generate a unique clOrdID with our prefix so we can identify it.
        clOrdID = self.orderIDPrefix + base64.b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=\n')
        if (side == 'Sell' and offset > 0) or (side == 'Buy' and offset < 0): offset = offset * -1
        postdict = {"execInst"      : "LastPrice",
                    "ordType"       : "StopMarket",
                    "pegOffsetValue": offset,
                    "pegPriceType"  : "TrailingStopPeg",
                    "orderQty"      : quantity,
                    "symbol"        : settings.BITMEX_SYMBOL,
                    "side"          : side,
                    "text"          : "automated trading",
                    'clOrdID'       : clOrdID}

        return self._curl_bitmex(api=endpoint, postdict=postdict, verb="POST")

    def position(self):
        return self.socket.position()

    def orders(self):
        return self.socket.orders()

    def _curl_bitmex(self, api, query=None, postdict=None, timeout=3, verb=None):
        """Send a request to BitMEX Servers."""
        # Handle URL
        url = settings.BITMEX_URL + api

        # Default to POST if data is attached, GET otherwise
        if not verb:
            verb = 'POST' if postdict else 'GET'

        auth = APIKeyAuthWithExpires.APIKeyAuthWithExpires(settings.BITMEX_API_KEY, settings.BITMEX_API_SECRET)

        # Make the request
        try:
            self.logger.debug("BITMEX REST: " + verb + " " + url + " " + ('' if postdict == None else json.dumps(postdict)) )
            req = requests.Request(verb, url, data=postdict, auth=auth, params=query)
            prepped = self.session.prepare_request(req)
            response = self.session.send(prepped, timeout=timeout)
            # Make non-200s throw
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            # 401 - Auth error. Re-auth and re-run this request.
            if response.status_code == 401:
                if self.token is None:
                    self.logger.error("Login information or API Key incorrect, please check and restart.")
                    self.logger.error("Error: " + response.text)
                    if postdict:
                        self.logger.error(postdict)
                    exit(1)
                self.logger.warning("Token expired, reauthenticating...")
                sleep(1)
                self.authenticate()
                return self._curl_bitmex(api, query, postdict, timeout, verb)

            # 404, can be thrown if order canceled does not exist.
            elif response.status_code == 404:
                if verb == 'DELETE':
                    self.logger.error("Order not found: %s" % postdict['orderID'])
                    return
                self.logger.error("Unable to contact the BitMEX API (404). " +
                                  "Request: %s \n %s" % (url, json.dumps(postdict)))
                exit(1)

            # 429, ratelimit
            elif response.status_code == 429:
                self.logger.error("Ratelimited on current request. Sleeping, then trying again. Try fewer " +
                                  "order pairs or contact support@bitmex.com to raise your limits. " +
                                  "Request: %s \n %s" % (url, json.dumps(postdict)))
                sleep(1)
                return self._curl_bitmex(api, query, postdict, timeout, verb)

            # 503 - BitMEX temporary downtime, likely due to a deploy. Try again
            elif response.status_code == 503:
                self.logger.warning("Unable to contact the BitMEX API (503), retrying. " +
                                    "Request: %s \n %s" % (url, json.dumps(postdict)))
                sleep(1)
                return self._curl_bitmex(api, query, postdict, timeout, verb)
            # Unknown Error
            else:
                self.logger.error("Unhandled Error: %s: %s" % (e, json.dumps(response.json(), indent=4)))
                self.logger.error("Endpoint was: %s %s" % (verb, api))
                exit(1)

        except requests.exceptions.Timeout as e:
            # Timeout, re-run this request
            self.logger.warning("Timed out, retrying...")
            return self._curl_bitmex(api, query, postdict, timeout, verb)

        except requests.exceptions.ConnectionError as e:
            self.logger.warning("Unable to contact the BitMEX API (ConnectionError). Please check the URL. Retrying. " +
                                "Request: %s \n %s" % (url, json.dumps(postdict)))
            sleep(1)
            return self._curl_bitmex(api, query, postdict, timeout, verb)

        return response.json()
