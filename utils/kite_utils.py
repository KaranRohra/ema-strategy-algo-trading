from utils.common import first
from connection import kite
from datetime import datetime as dt, timedelta as td


def get_holding_by_symbol(exchange, symbol):
    positions = [p for p in kite.positions()["net"] if p["quantity"] != 0]
    positions.extend(kite.holdings())

    return first(
        [
            p
            for p in positions
            if p["tradingsymbol"] == symbol and p["exchange"] == exchange
        ]
    )


def get_ohlc(instrument_token, interval="5minute"):
    return kite.historical_data(
        instrument_token=instrument_token,
        interval=interval,
        from_date=dt.now() - td(days=7),
        to_date=dt.now(),
    )[-1]


def get_historical_data(instrument_token, interval, mod):
    now = dt.now()
    from_date = now - td(days=80)
    to_date = now.replace(minute=now.minute - now.minute % mod)
    return kite.historical_data(
        instrument_token=instrument_token,
        interval=interval,
        from_date=from_date,
        to_date=to_date,
    )


def get_order_status(order_id):
    return first([o for o in kite.orders() if o["order_id"] == order_id])


def get_basket_items():
    return first([b for b in kite.baskets() if b["name"] == "algo-trading"])["items"]


def get_candle_interval(time_frame) -> str:
    return {
        1: "minute",
        3: "3minute",
        5: "5minute",
        10: "10minute",
        15: "15minute",
        30: "30minute",
        60: "60minute",
    }[time_frame]
