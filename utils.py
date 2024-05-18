import os

from os import environ
from constants import kite, Env
from datetime import datetime as dt, timedelta as td


def first(lst: list) -> list | None:
    return lst[0] if lst else None


def last(lst: list) -> list | None:
    return lst[-1] if lst else None


def get_product_type() -> str:
    if os.environ.get(Env.PRODUCT_TYPE):
        return os.environ[Env.PRODUCT_TYPE]
    if os.environ[Env.SEGMENT] == "EQ":
        return kite.PRODUCT_CNC
    if os.environ[Env.SEGMENT] == "F&O":
        return kite.PRODUCT_NRML


# KITE UTILS
class KiteUtils:
    @staticmethod
    def get_holding_by_symbol(symbol):
        positions = [p for p in kite.positions()["net"] if p["quantity"] != 0]
        positions.extend(kite.holdings())

        return first([p for p in positions if p["tradingsymbol"] == symbol])

    @staticmethod
    def get_instrument_token(exchange, symbol):
        symbol = f"{exchange}:{symbol}"
        return kite.ltp([symbol])[symbol]["instrument_token"]

    @staticmethod
    def get_historical_data(
        exchange,
        symbol,
        interval,
        from_date,
        to_date,
    ):
        return kite.historical_data(
            instrument_token=KiteUtils.get_instrument_token(exchange, symbol),
            interval=interval,
            from_date=from_date,
            to_date=to_date,
        )

    @staticmethod
    def get_order_status(order_id):
        return first([o for o in kite.orders() if o["order_id"] == order_id])


class MarketUtils:
    @staticmethod
    def is_market_open() -> bool:
        now = dt.now()
        TIME_FORMAT = "%H:%M:%S"
        start_time = dt.strptime(environ[Env.START_TIME], TIME_FORMAT)
        start_time = start_time.replace(year=now.year, month=now.month, day=now.day)

        end_time = dt.strptime(environ[Env.END_TIME], TIME_FORMAT)
        end_time = end_time.replace(year=now.year, month=now.month, day=now.day)

        market_open = start_time <= now <= end_time
        if not market_open:
            print(
                f"Market is closed: {now} - Market timings: {start_time} - {end_time}"
            )
        return market_open

    @staticmethod
    def get_candle_interval(time_frame) -> str:
        return {
            "1": "minute",
            "day": "day",
            "3": "3minute",
            "5": "5minute",
            "10": "10minute",
            "15": "15minute",
            "30": "30minute",
            "60": "60minute",
        }[time_frame]
