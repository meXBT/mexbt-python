import hmac
import json
import time
import hashlib

import requests

class Mexbt:

    def __init__(self, pair=None, sandbox=False, **kwargs):
        for key, value in kwargs.iteritems():
            if any(key in i for i in ['public_key', 'private_key', 'user_id']):
                setattr(self, key, value)

        self._default_pair = pair if pair is not None else 'btcmxn'

        self._public_url = 'https://public-api.mexbt.com'
        if sandbox:
            self._private_url = 'https://private-api-sandbox.mexbt.com'
        else:
            self._private_url = 'https://private-api.mexbt.com'

    def _url(self, base, endpoint):
        return '%s/v1/%s' % (base, endpoint)

    def _call(self, url, params):
        result = requests.post(url, data=json.dumps(params))
        if result.status_code != 200:
            raise Exception('Unexpected response from the API')
        json_response = result.json()
        if json_response['isAccepted']:
            return json_response
        else:
            raise Exception('API request rejected: %s' % json_response['rejectReason'])

    def _public(self, endpoint, **kwargs):
        return self._call(self._url(self._public_url, endpoint), kwargs)

    def _private(self, endpoint, **kwargs):
        for k in ('public_key', 'private_key', 'user_id'):
            if getattr(self, k) is None:
                raise Exception('You must configure %s to make private calls' % k)

        nonce = int(time.time() * 10000)
        sign = hmac.new(self.private_key,
                        '%s%s%s' % (nonce, self.user_id, self.public_key),
                        hashlib.sha256).hexdigest().upper()
        params = {'apiKey': self.public_key, 'apiNonce': nonce, 'apiSig': sign}

        kwargs.update(params)
        return self._call(self._url(self._private_url, endpoint), kwargs)


    # Public calls

    def ticker(self, pair=None):
        return self._public("ticker", productPair=pair or self._default_pair)

    def order_book(self, pair=None):
        return self._public("order-book", productPair=pair or self._default_pair)

    orderbook = order_book
    orders = order_book

    def currency_pairs(self):
        return self._public("product-pairs")

    def trades(self, pair=None, start_index=-1, count=10):
        pair = pair or self._default_pair
        return self._public('trades', ins=pair, startIndex=start_index,
                            count=count)

    public_trades = trades

    def trades_by_date(self, from_date, to_date, pair=None):
        params = {
            'ins': pair or self._default_pair,
            'startDate': from_date,
            'endDate': to_date
        }
        return self._public("trades-by-date", **params)


    # Private calls

    def create_order(self, amount, side='buy', price=None, pair=None, order_type='market'):
        params = {
            'ins': pair or self._default_pair,
            'side': side,
            'qty': amount
        }
        if order_type == 'market' or order_type == 1:
            params['orderType'] = 1
        elif order_type == 'limit' or order_type == 0:
            params['orderType'] = 0
        else:
            raise Exception("Unknown order type '%s'" % otype)
        if price is not None:
            params['px'] = price
        return self._private('orders/create', **params)

    def cancel_order(self, oid, pair=None):
        pair = pair or self._default_pair
        return self._private('orders/cancel', serverOrderId=oid, ins=pair)

    def cancel_all_orders(self, pair=None):
        pair = pair or self._default_pair
        return self._private('orders/cancel-all', ins=pair)

    def modify_order(self, oid, action, pair=None):
        pair = pair or self._default_pair
        if action == 'move_to_top' or action == 0:
            action = 0
        elif action == 'execute_now' or action == 1:
            action = 1
        else:
            raise Exception("action must be one of 'move_to_top', 'execute_now'")
        return self._private('orders/modify', ins=pair, serverOrderId=id,
                             modifyAction=action)

    def account_trades(self, pair=None, start_index=-1, count=10):
        """Return the trade history for this account."""
        pair = pair or self._default_pair
        return self._private('trades', ins=pair, startIndex=start_index,
                             count=count)

    def account_info(self):
        """Fetches account information."""
        return self._private('me')

    def account_balance(self):
        """Fetches balance information."""
        return self._private('balance')

    def account_orders(self):
        """Fetches open orders."""
        return self._private('orders')

    def account_addresses(self):
        """Return deposit addresses for this account."""
        return self._private('deposit-addresses')

    def withdraw(self, amount, address, currency='btc'):
        return self._private('withdraw', ins=currency, amount=amount,
                             sendToAddress=address)
