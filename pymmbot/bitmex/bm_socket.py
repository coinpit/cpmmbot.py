import json
import logging
import threading
import traceback
from urllib.parse import urlparse

import websocket

from pymmbot.bitmex.auth import APIKeyAuth
from settings import settings


class BM_Socket(object):
    def __init__(self):
        self.callbacks = {}
        self.data = {}
        self.keys = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self, callbacks):
        # We can subscribe right in the connection querystring, so let's build that.
        # Subscribe to all pertinent endpoints
        url = settings.BITMEX_URL
        symbol = 'XBTU17'
        subscriptions = [sub + ':' + symbol for sub in settings.BITMEX_TOPICS]
        # subscriptions += ["margin"]

        parsed = urlparse(url)
        socket_url = 'wss://' + parsed.hostname + "/realtime?subscribe=" + ",".join(subscriptions)
        self.callbacks = callbacks
        ws = websocket.WebSocketApp(socket_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_open=self.on_open,
                                    header=self.__get_auth()
                                    )
        self.wst = threading.Thread(target=lambda: ws.run_forever())
        self.wst.daemon = True
        self.wst.start()
        print("Started thread")

    def __get_auth(self):
        self.logger.info("Authenticating with API Key.")
        # To auth to the WS using an API key, we generate a signature of a nonce and
        # the WS API endpoint.
        nonce = APIKeyAuth.generate_nonce()
        return [
            "api-nonce: " + str(nonce),
            "api-signature: " + APIKeyAuth.generate_signature(settings.BITMEX_API_SECRET, 'GET', '/realtime', nonce,
                                                              ''),
            "api-key:" + settings.BITMEX_API_KEY
        ]

    def on_message(self, ws, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        self.logger.debug(json.dumps(message))

        table = message['table'] if 'table' in message else None
        action = message['action'] if 'action' in message else None
        try:
            if 'subscribe' in message:
                if message['success']:
                    self.logger.debug("Subscribed to %s." % message['subscribe'])
                else:
                    self.error("Unable to subscribe to %s. Error: \"%s\" Please check and restart." %
                               (message['request']['args'][0], message['error']))
            elif 'status' in message:
                if message['status'] == 400:
                    self.error(message['error'])
                if message['status'] == 401:
                    self.error("Login information or API Key incorrect, please check and restart.")
            elif action:

                if table not in self.data:
                    self.data[table] = []

                if table not in self.keys:
                    self.keys[table] = []

                # There are four possible actions from the WS:
                # 'partial' - full table image
                # 'insert'  - new row
                # 'update'  - update row
                # 'delete'  - delete row
                if action == 'partial':
                    self.logger.debug("%s: partial" % table)
                    self.data[table] += message['data']
                    # Keys are communicated on partials to let you know how to uniquely identify
                    # an item. We use it for updates.
                    self.keys[table] = message['keys']
                elif action == 'insert':
                    self.logger.debug('%s: inserting %s' % (table, message['data']))
                    self.data[table] += message['data']
                elif action == 'update':
                    self.logger.debug('%s: updating %s' % (table, message['data']))
                    # Locate the item in the collection and update it.
                    for updateData in message['data']:
                        item = findItemByKeys(self.keys[table], self.data[table], updateData)
                        if not item:
                            return  # No item found to update. Could happen before push
                        item.update(updateData)
                        # Remove cancelled / filled orders
                        if table == 'order' and item['leavesQty'] <= 0:
                            self.data[table].remove(item)
                elif action == 'delete':
                    self.logger.debug('%s: deleting %s' % (table, message['data']))
                    # Locate the item in the collection and remove it.
                    for deleteData in message['data']:
                        item = findItemByKeys(self.keys[table], self.data[table], deleteData)
                        self.data[table].remove(item)
                else:
                    raise Exception("Unknown action: %s" % action)
        except:
            self.logger.error(traceback.format_exc())

        if table:
            if message['table'] == 'orderBook10':
                # print(message['action'], message['data'][0]['symbol'], message['data'][0]['bids'][0], len(message['data'][0]['bids']), message['data'][0]['asks'][0], len(message['data'][0]['asks']))
                if 'orderBook10' in self.callbacks:  self.callbacks['orderBook10'](message['data'][0])
            elif message['table'] == 'position':
                if 'position' in self.callbacks:  self.callbacks['position'](message['data'][0])
            elif message['table'] == 'order':
                print('order:', message)

    def on_error(self, message):
        self.logger.debug("Websocket error.")

    def on_close(self, message):
        self.logger.debug("Websocket Closed.")

    def on_open(self, message):
        self.logger.debug("Websocket Opened.")

    def error(self, err):
        self._error = err
        self.logger.error(err)

    def position(self):
        return self.data['position']

    def orders(self):
        return self.data['order']


def findItemByKeys(keys, table, matchData):
    for item in table:
        matched = True
        for key in keys:
            if item[key] != matchData[key]:
                matched = False
        if matched:
            return item
