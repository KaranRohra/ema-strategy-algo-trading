import os
import market_utils
import time

from dotenv import load_dotenv
from constants import Holding, Trade, Env
from strategy.entry import get_analyzed_params
from orders import orders
from kite import utils as kite_utils
from datetime import datetime as dt
from db import mongodb
from mail.app import Mail


load_dotenv()


def dump_candle_data(candle_data):
    mongodb.MongoDB.candle_collection.insert_one(candle_data)


def dump_holding_data(entry_details, send_email=True):
    mongodb.MongoDB.holding_cache = None
    mongodb.MongoDB.holding_collection.insert_one(entry_details)
    if send_email:
        Mail.send_entry_email(entry_details)


def dump_trade_data(exit_details, send_email=True):
    acknowledged = mongodb.MongoDB.trade_collection.insert_one(
        exit_details
    ).acknowledged
    mongodb.MongoDB.holding_cache = None
    if acknowledged:
        mongodb.MongoDB.holding_collection.delete_one(
            {Holding.SYMBOL: exit_details[Trade.SYMBOL]}
        )
        if send_email:
            Mail.send_exit_email(exit_details)


def start_trading():
    symbol = os.environ[Env.SYMBOL]
    exchange = os.environ[Env.EXCHANGE]

    is_trading_started_mail_sent = False
    while market_utils.get_market_status()["open"]:
        if not market_utils.is_trading_time():
            continue

        if not is_trading_started_mail_sent:
            Mail.send_trading_started_email()
            is_trading_started_mail_sent = True

        now = dt.now()

        # Run for every 5 minute (5 minute candle)
        if now.minute % 5 == 0 and now.second == 0:
            ohlc = kite_utils.get_historical_data(exchange, symbol)
            if kite_utils.get_holding(symbol):
                exit_details = orders.exit_order(exchange, symbol, ohlc)
                if exit_details["signal"] in (
                    Trade.EXIT_LONG_POSITION,
                    Trade.EXIT_SHORT_POSITION,
                ):
                    dump_trade_data(exit_details)
            else:
                entry_details = orders.entry_order(exchange, symbol, ohlc)
                if entry_details["signal"] in (
                    Holding.ENTER_LONG_POSITION,
                    Holding.ENTER_SHORT_POSITION,
                ):
                    dump_holding_data(entry_details)
            dump_candle_data(get_analyzed_params(exchange, symbol, ohlc))
            print(now.strftime("%Y-%m-%d %H:%M:%S") + " - Candle data dumped...")
            time.sleep(1)

    print("Market is closed due to: " + market_utils.get_market_status()["reason"])
    Mail.send_market_close_email(market_utils.get_market_status()["reason"])
