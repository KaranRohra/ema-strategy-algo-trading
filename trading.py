import os
import orders
import time

from constants import Env, LogType
from datetime import datetime as dt, timedelta
from utils import kite_utils, market_utils as mu
from mail import app as ma
from db import MongoDB


def trading_start_notification(exchange, symbol):
    trade_details = {
        "exchange": exchange,
        "symbol": symbol,
        "entry_time_frame": os.environ[Env.ENTRY_TIME_FRAME] + "minutes",
        "exit_time_frame": os.environ[Env.EXIT_TIME_FRAME] + "minutes",
    }
    ma.send_trading_started_email(**trade_details)
    MongoDB.insert_log(
        log_type=LogType.INFO, message="Trading started"
    )


def start():
    symbol_details = kite_utils.get_basket_item()
    exchange, symbol = symbol_details["exchange"], symbol_details["tradingsymbol"]

    trading_start_notification(exchange, symbol)
    entry_time_frame = int(os.environ[Env.ENTRY_TIME_FRAME])
    exit_time_frame = int(os.environ[Env.EXIT_TIME_FRAME])

    while mu.is_market_open()["is_market_open"]:
        now = dt.now()
        if now.minute % entry_time_frame == 0 and now.second == 0:
            holding = kite_utils.get_holding_by_symbol(exchange, symbol)
            if not holding:
                orders.search_entry(symbol_details)
        if now.minute % exit_time_frame == 0 and now.second == 0:
            holding = kite_utils.get_holding_by_symbol(exchange, symbol)
            if holding:
                orders.search_exit(holding)
        time.sleep(1)

    end_time = mu.is_market_open()["end_time"] + timedelta(minutes=1)
    if end_time > dt.now():
        holding = kite_utils.get_holding_by_symbol(exchange, symbol)
        if holding:
            orders.search_exit(holding)
        else:
            orders.search_entry(symbol_details)
