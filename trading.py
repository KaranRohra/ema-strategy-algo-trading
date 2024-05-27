import os
import orders
import time

from constants import Env, kite
from datetime import datetime as dt, timedelta
from utils import kite_utils, market_utils


def search_trade(candle_interval, time_frame, symbol, exchange, instrument_token):
    now = dt.now()
    from_date = now - timedelta(days=90)
    to_date = now.replace(minute=now.minute - now.minute % int(time_frame))
    ohlc = kite.historical_data(
        instrument_token=instrument_token,
        interval=candle_interval,
        from_date=from_date,
        to_date=to_date,
    )

    holding = kite_utils.get_holding_by_symbol(exchange, symbol)
    if holding:
        orders.search_exit(ohlc, holding)
    else:
        orders.search_entry(ohlc)
    print("*" * 20)
    print(f"Waiting for next candle - Current time: {now}")


def start():
    symbol_details = kite_utils.get_basket_item()
    exchange, symbol = symbol_details["exchange"], symbol_details["tradingsymbol"]
    instrument_token = symbol_details["instrument_token"]

    time_frame = os.environ[Env.TIME_FRAME]
    candle_interval = market_utils.get_candle_interval(time_frame)
    print(
        f"Starting trading on {exchange} with {symbol} on {candle_interval} time frame"
    )

    while market_utils.is_market_open()["is_market_open"]:
        now = dt.now()
        if now.minute % 5 == 0 and now.second == 0:
            search_trade(
                candle_interval,
                time_frame,
                symbol,
                exchange,
                instrument_token,
            )
        time.sleep(1)

    market_status = market_utils.is_market_open()
    if dt.now() >= market_status["end_time"] and dt.now() < market_status[
        "end_time"
    ].replace(
        minute=market_status["end_time"].minute + 2
    ):  # Execute last trade before market closes
        search_trade(
            candle_interval,
            1,
            symbol,
            exchange,
            instrument_token,
        )
    print("Market closed...")
