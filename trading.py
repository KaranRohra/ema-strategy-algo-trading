import os
import orders
import time

from constants import Env
from datetime import datetime as dt
from utils import KiteUtils, MarketUtils


def start():
    exchange, symbol = os.environ[Env.EXCHANGE], os.environ[Env.SYMBOL]
    print(f"Starting trading on {exchange} with {symbol}")

    while MarketUtils.is_market_open():
        now = dt.now()
        if now.minute % 5 == 0 and now.second == 0:
            ohlc = KiteUtils.get_historical_data(exchange, symbol)
            holding = KiteUtils.get_holding_by_symbol(symbol)
            if holding:
                orders.search_exit(ohlc, holding)
            else:
                orders.search_entry(exchange, symbol, ohlc)
            print("*" * 20)
            print(f"Waiting for next candle {now}")
        time.sleep(1)
