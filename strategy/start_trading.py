import os
import utils
import time

from dotenv import load_dotenv
from constants import Holding, Trade
from strategy.entry import get_analyzed_params
from orders import orders
from kite_utils import kite_utils
from datetime import datetime as dt
from db import mongodb


load_dotenv()


def dump_candle_data(exchange, symbol):
    mongodb.MongoDB.candle_collection.insert_one(get_analyzed_params(exchange, symbol))


def dump_holding_data(entry_details):
    mongodb.MongoDB.holding_collection.insert_one(entry_details)


def dump_trade_data(exit_details):
    acknowledged = mongodb.MongoDB.trade_collection.insert_one(
        exit_details
    ).acknowledged
    if acknowledged:
        mongodb.MongoDB.holding_collection.delete_one(
            {Holding.SYMBOL: exit_details[Trade.SYMBOL]}
        )


def start_trading():
    symbol = os.environ["SYMBOL"]
    exchange = os.environ["EXCHANGE"]

    while utils.get_market_status()["open"]:
        if not utils.is_trading_time():
            continue

        now = dt.now()

        # Run for every 5 minute (5 minute candle)
        if now.minute % 5 == 0 and now.second == 0:
            if kite_utils.get_holding(symbol):
                exit_details = orders.exit_order(exchange, symbol)
                if exit_details:
                    dump_trade_data(exit_details)
            else:
                entry_details = orders.entry_order(exchange, symbol)
                if entry_details:
                    dump_holding_data(entry_details)

            dump_candle_data(exchange, symbol)
            print(now.strftime("%Y-%m-%d %H:%M:%S") + " - Candle data dumped...")
            time.sleep(1)
    else:
        print("Market is closed due to: " + utils.get_market_status()["reason"])
