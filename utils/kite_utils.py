from utils.common import first
from datetime import datetime as dt, timedelta as td
from kite.connect import KiteConnect
from typing import List
from gsheet import users as gusers


def get_holding(positions, holdings, instrument_token):
    positions = [p for p in positions["net"] if p["quantity"] != 0]
    positions.extend(holdings)

    return first([p for p in positions if p["instrument_token"] == instrument_token])


def get_ohlc(kite: KiteConnect, instrument_token, interval="5minute"):
    return kite.historical_data(
        instrument_token=instrument_token,
        interval=interval,
        from_date=dt.now() - td(days=7),
        to_date=dt.now(),
    )[-1]


def get_historical_data(kite: KiteConnect, instrument_token, interval):
    now = dt.now()
    candle_interval = get_candle_interval(interval)
    from_date = now - td(days=candle_interval["day_limit"])
    to_date = now - td(minutes=1)
    return kite.historical_data(
        instrument_token=instrument_token,
        interval=candle_interval["interval"],
        from_date=from_date,
        to_date=to_date,
    )


def get_order_status(kite: KiteConnect, order_id):
    return first([o for o in kite.orders() if o["order_id"] == order_id])


def get_basket_items(user: gusers.User, name: str):
    basket = first([b for b in user.kite.baskets() if b["name"] == name])
    if basket:
        return basket["items"]

    print(f"[{dt.now()}] [{user.user_id}]: Basket not found - {name}")
    return []


def get_candle_interval(time_frame) -> str:
    return {
        1: {"interval": "minute", "day_limit": 5},
        3: {"interval": "3minute", "day_limit": 15},
        5: {"interval": "5minute", "day_limit": 30},
        10: {"interval": "10minute", "day_limit": 60},
        15: {"interval": "15minute", "day_limit": 90},
        30: {"interval": "30minute", "day_limit": 90},
        60: {"interval": "60minute", "day_limit": 90},
    }[time_frame]
