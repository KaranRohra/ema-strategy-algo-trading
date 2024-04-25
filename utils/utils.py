import math
import pandas as pd

from constants import *
from config import *
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


def is_symbol_in_holdings_or_position():
    holdings_df = pd.read_csv(HOLDINGS_CSV_PATH)
    return holdings_df.size and SYMBOL in holdings_df[HOLDING_SYMBOL].values


def get_qty(entry, stoploss, available_capital):
    qty = math.abs(RISK_AMOUNT // (entry - stoploss))
    required_capital = qty * entry

    if required_capital >= available_capital:
        return available_capital // entry

    return qty
