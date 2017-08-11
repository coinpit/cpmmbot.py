import logging
from pymmbot.bitmex import bitmex
from pymmbot.coinpit import coinpit
from pymmbot.settings import settings
from easydict import EasyDict as edict
from pymmbot.utils import common_util
import math
import traceback
import sys
import time

# import logging.config
# from os import path

LATCH_ORDER = 'latchorder'


class MMBot(object):
    def __init__(self):
        # log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
        # logging.config.fileConfig(log_file_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.bitmex = bitmex.Bitmex()
        self.coinpit = coinpit.Coinpit()
        self.current_spread = None
        self.current_price = {'buy': None, 'sell': None}

    def connect(self):
        self.coinpit.connect(edict({
            'account': self.coinpit_account_change,
            'index'  : self.coinpit_index_change,
            'del'    : self.coinpit_order_del
        }))
        self.bitmex.connect(edict({
            'orderBook10': self.on_bitmex_orderbook_change,
            'position'   : self.on_bitmex_position
        }))

    def initiate(self):
        while True:
            time.sleep(settings.HEDGE_INTERVAL)
            try:
                self.replenish_coinpit_limit_orders()
            except Exception as e:
                self.logger.exception("replenish_coinpit_limit_orders failed.")
            try:
                self.hedge_on_bitmex()
            except:
                self.logger.exception("hedge_on_bitmex failed.")

    def coinpit_account_change(self):
        # self.replenish_coinpit_limit_orders()
        # self.hedge_on_bitmex()
        pass

    def coinpit_index_change(self):
        # self.replenish_coinpit_limit_orders()
        pass

    def coinpit_order_del(self):
        pass
        # self.replenish_coinpit_limit_orders()

    def on_bitmex_orderbook_change(self, data):
        try:
            if data is None or 'bids' not in data or 'asks' not in data:
                self.logger.debug("Invalid orderbook from bitmex %s", data)
                return
            buy_price = self.get_price_for(
                settings.COINPIT_QTY * settings.COINPIT_BITMEX_RATIO * settings.QUANTITY_MULTIPLIER,
                data['bids'])
            sell_price = self.get_price_for(
                settings.COINPIT_QTY * settings.COINPIT_BITMEX_RATIO * settings.QUANTITY_MULTIPLIER,
                data['asks'])
            self.current_spread = round(sell_price - buy_price, settings.COINPIT_TICK_SIZE)
        except Exception as e:
            self.logger.exception('on_bitmex_orderbook_change')
            # self.replenish_coinpit_limit_orders()

    def on_bitmex_position(self):
        self.logger.debug('bitmex position %s', self.bitmex.position())
        # self.hedge_on_bitmex()

    def replenish_coinpit_limit_orders(self):
        if self.coinpit.index() is None or self.current_spread is None: return
        premium = self.get_current_premium()
        buy = round(self.coinpit.index() - self.current_spread / 2 + premium, settings.COINPIT_TICK_SIZE)
        sell = round(self.coinpit.index() + self.current_spread / 2 + premium, settings.COINPIT_TICK_SIZE)
        self.send_orders_to_coinpit(buy, sell)

    def send_orders_to_coinpit(self, buy_price, sell_price):
        orders = self.get_current_bid_ask()
        updates = []
        adds = []
        self.populate_replace_add_for_coinpit('buy', buy_price, orders['buys'], updates, adds)
        self.populate_replace_add_for_coinpit('sell', sell_price, orders['sells'], updates, adds)
        self.update_latch(updates, adds)
        patch = []
        if len(updates) > 0:
            patch.append({'op': 'replace', 'value': updates})
        if len(adds) > 0:
            patch.append({'op': 'add', 'value': adds})
        if len(patch) > 0:
            self.coinpit.rest.auth_server_call('PATCH', '/order', patch)

    def update_latch(self, updates, adds):
        if self.coinpit.index() is None: return
        latch_diff = self.coinpit.index() * settings.COINPIT_LATCH
        buy_price = round(self.coinpit.index() - latch_diff, settings.COINPIT_TICK_SIZE)
        sell_price = round(self.coinpit.index() + latch_diff, settings.COINPIT_TICK_SIZE)
        orders = self.get_latch_orders()
        self.add_or_update_latch('buy', buy_price, updates, adds, orders)
        self.add_or_update_latch('sell', sell_price, updates, adds, orders)

    def add_or_update_latch(self, side, price, updates, adds, orders):
        order = orders[side]
        if order is None:
            adds.append({
                "instrument" : settings.COINPIT_SYMBOL,
                "side"       : side,
                "quantity"   : 1,
                "price"      : price,
                "orderType"  : "LMT",
                "crossMargin": True,
                "targetPrice": "NONE",
                "clientid"   : side + LATCH_ORDER
            })
        elif order['price'] != price:
            updates.append({'uuid': order['uuid'], 'price': price})

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
        for uuid in self.coinpit.user_details['orders'][instrument]:
            order = self.coinpit.user_details['orders'][instrument][uuid]
            if order is not None and order['orderType'] == 'LMT' and is_latch_order(order) == False:
                side = orders['buys'] if order['side'] == 'buy' else orders['sells']
                side.insert(0, order)
        return orders

    def get_latch_orders(self):
        orders = {'buy': None, 'sell': None}
        instrument = self.get_coinpit_instrument()
        for uuid in self.coinpit.user_details['orders'][instrument]:
            order = self.coinpit.user_details['orders'][instrument][uuid]
            if order is not None and order['orderType'] == 'LMT' and is_latch_order(order):
                orders[order['side']] = order
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

    # premium = current_index * interest_rate * days_left /365
    def get_current_premium(self):
        symbol = self.get_coinpit_instrument()
        instrument = self.coinpit.config['instruments'][symbol]
        expiry = instrument['expiry']
        current = common_util.current_milli_time()
        diff = expiry - current
        days = math.ceil(diff / (24 * 60 * 60 * 1000))
        premium = self.coinpit.index() * settings.INTEREST_RATE * days / 365
        return round(premium, settings.COINPIT_TICK_SIZE)

    def hedge_on_bitmex(self):
        if self.coinpit.user_details is None: return
        positions = self.coinpit.user_details['positions']
        instrument = self.get_coinpit_instrument()
        position = None if instrument not in positions else positions[instrument]
        on_coinpit = 0 if position is None else position['quantity']
        on_bitmex = self.get_total_position_in_bitmex()
        hedge_count = on_bitmex + on_coinpit * settings.COINPIT_BITMEX_RATIO
        if self.already_hedged(hedge_count): return
        if len(self.bitmex.orders()) > 0: self.bitmex.cancel_all_orders()
        side = 'Sell' if hedge_count > 0 else 'Buy'
        if self.bitmex: self.bitmex.place_order(abs(hedge_count), side, settings.BITMEX_TRAILING_PEG)

    def get_total_position_in_bitmex(self):
        position = self.bitmex.position()[0]
        return position['currentQty']

    @staticmethod
    def get_available_qty(orders):
        available = 0
        for order in orders:
            available = available + order['quantity'] - order['filled'] - order['cancelled']
        return available

    def get_coinpit_instrument(self):
        assert (self.coinpit.config is not None and 'alias' in self.coinpit.config), 'coinpit_config not set'
        return self.coinpit.config['alias'][settings.COINPIT_SYMBOL]

    def already_hedged(self, hedge_count):
        hedged = 0
        for order in self.bitmex.orders():
            hedged = order['orderQty'] * (-1 if order['side'] == 'Buy' else 1)
        return hedge_count == hedged


def is_latch_order(order):
    return True if 'clientid' in order and order['clientid'].endswith(LATCH_ORDER) else False
