# meXBT Python client

This is a lightweight Python client for the [meXBT](https://mexbt.com) exchange API. It doesn't try and do anything clever with the JSON response from the API, it simply
returns it as-is.

## Install

    pip install mexbt


## Setup

If you only need to access public data, you don't need to configure credentials:

```python
from mexbt import Mexbt
api = Mexbt(pair='btcmxn') # You can actually leave this out as btcmxn is the default
```

If you want to access private data, configure credentials like this:

```python
from mexbt import Mexbt
api = Mexbt(public_key='foo', private_key='bar', user_id='123', sandbox=True)
```

## Public API

```python
api.ticker()
api.orders()
api.trades()
api.currency_pairs()
api.currency_pairs()
```

## Private API

```python
api.create_order(1234.56, pair='btcmxn', side='buy', order_type='market')
api.cancel_order(123)
api.cancel_all_orders()
api.modify_order(123, 'move_to_top')
api.modify_order(123, 'execute_now')
api.account_info()
api.account_balance()
api.account_orders()
api.account_trades(start_index=-1, count=10)
api.account_addresses()
api.withdraw(1.23456789, 'foo')
```
