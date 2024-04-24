from datetime import datetime, timedelta
from config import *


def get_instrument_token():
    kite_symbol = f"{EXCHANGE}:{SYMBOL}"
    return kite.ltp(kite_symbol)[kite_symbol]["instrument_token"]


def get_ltp():
    kite_symbol = f"{EXCHANGE}:{SYMBOL}"
    return kite.ltp(kite_symbol)[kite_symbol]["last_price"]


def get_historical_data(interval="5minute", last_day=95):
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute - now.minute % 5)
    return kite.historical_data(
        instrument_token=get_instrument_token(),
        from_date=now - timedelta(days=last_day),
        to_date=now,
        interval=interval,
    )
