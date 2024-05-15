import os

from constants import kite, Env
from datetime import datetime as dt, timedelta as td


def first(lst: list) -> list | None:
    return lst[0] if lst else None


def last(lst: list) -> list | None:
    return lst[-1] if lst else None


def get_product_type() -> str:
    if os.environ[Env.SEGMENT] == "EQ":
        return kite.PRODUCT_CNC
    elif os.environ[Env.SEGMENT] == "F&O":
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
        interval="5minute",
        from_date=dt.now() - td(days=95),
        to_date=dt.now(),
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
