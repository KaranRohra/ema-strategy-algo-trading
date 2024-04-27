import math
import os

from datetime import datetime, time


def is_market_open():
    now = datetime.now().time()
    market_open_time = time(9, 15, 0)
    market_end_time = time(15, 29, 30)

    return now >= market_open_time and now <= market_end_time


def is_trading_time():
    now = datetime.now().time()
    market_open_time = time(9, 0, 0)
    market_end_time = time(15, 30, 30)

    return now >= market_open_time and now <= market_end_time


def get_qty(entry, stoploss, available_capital):
    risk_amount = os.environ.get("RISK_AMOUNT", 1000)
    qty = math.abs(risk_amount // (entry - stoploss))
    required_capital = qty * entry

    if required_capital >= available_capital:
        return available_capital // entry

    return qty
