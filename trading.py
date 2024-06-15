import os
import orders
import time

from constants import Env, LogType
from datetime import datetime as dt, timedelta
from utils import kite_utils, market_utils as mu
from mail import app as ma
from db import MongoDB


def trading_start_notification(basket_items):
    trade_details_lst = [
        {
            "heading": "Time Frame",
            "key_value": {
                "entry_time_frame": os.environ[Env.ENTRY_TIME_FRAME] + "minutes",
                "exit_time_frame": os.environ[Env.EXIT_TIME_FRAME] + "minutes",
            },
        }
    ]

    for sd in basket_items:
        trade_details_lst.append(
            {
                "heading": "Symbol Details" if len(trade_details_lst) == 1 else "",
                "key_value": {
                    "exchange": sd["exchange"],
                    "symbol": sd["tradingsymbol"],
                },
            }
        )

    ma.send_trading_started_email(trade_details_lst)
    MongoDB.insert_log(
        log_type=LogType.INFO, message="Trading started", details=[d["key_value"] for d in trade_details_lst]
    )


def start():
    entry_time_frame = int(os.environ[Env.ENTRY_TIME_FRAME])
    exit_time_frame = int(os.environ[Env.EXIT_TIME_FRAME])

    basket_items = kite_utils.get_basket_items()
    trading_start_notification(basket_items)

    while mu.is_market_open()["is_market_open"]:
        now = dt.now()
        for sd in basket_items:  # SD = Symbol Details
            exchange, symbol = sd["exchange"], sd["tradingsymbol"]
            if now.minute % entry_time_frame == 0 and now.second == 0:
                holding = kite_utils.get_holding_by_symbol(exchange, symbol)
                if not holding:
                    orders.search_entry(sd)
            if now.minute % exit_time_frame == 0 and now.second == 0:
                holding = kite_utils.get_holding_by_symbol(exchange, symbol)
                if holding:
                    orders.search_exit(holding)
        time.sleep(1)

    end_time = mu.is_market_open()["end_time"] + timedelta(minutes=1)
    if end_time > dt.now():
        for sd in basket_items:  # SD = Symbol Details
            exchange, symbol = sd["exchange"], sd["tradingsymbol"]
            holding = kite_utils.get_holding_by_symbol(exchange, symbol)
            if holding:
                orders.search_exit(holding)
            else:
                orders.search_entry(sd)
