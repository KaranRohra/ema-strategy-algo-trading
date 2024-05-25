import os
import orders
import time

from constants import Env, kite
from datetime import datetime as dt, timedelta
from utils import KiteUtils, MarketUtils


def search_trade(candle_interval, time_frame, symbol, exchange, now):
    from_date = now - timedelta(days=90)
    to_date = now.replace(minute=now.minute - now.minute % int(time_frame))
    ohlc = kite.historical_data(
        instrument_token=os.environ[Env.INSTRUMENT_TOKEN],
        interval=candle_interval,
        from_date=from_date,
        to_date=to_date,
    )

    holding = KiteUtils.get_holding_by_symbol(exchange, symbol)
    if holding:
        orders.search_exit(ohlc, holding)
    else:
        orders.search_entry(exchange, symbol, ohlc)
    print("*" * 20)
    print(f"Waiting for next candle {now}")


def start():
    exchange, symbol = os.environ[Env.EXCHANGE], os.environ[Env.SYMBOL]
    time_frame = os.environ[Env.TIME_FRAME]
    candle_interval = MarketUtils.get_candle_interval(time_frame)
    print(
        f"Starting trading on {exchange} with {symbol} on {candle_interval} time frame"
    )

    while MarketUtils.is_market_open():
        now = dt.now()
        if now.minute % 5 == 0 and now.second == 0:
            search_trade(candle_interval, time_frame, symbol, exchange, now)
        time.sleep(1)
    
    # if 
