import os
import pandas as pd
from datetime import datetime as dt, timedelta

from constants import Env
from kite import utils as kite_utils
from constants import kite
from db import mongodb
from strategy import entry, exit


def start_back_testing(from_date, to_date):
    mongodb.MongoDB.holding_collection.delete_many({})
    mongodb.MongoDB.trade_collection.delete_many({})

    symbol = os.environ[Env.SYMBOL]
    exchange = os.environ[Env.EXCHANGE]

    candle_data = get_historical_data_for_back_testing(
        exchange, symbol, from_date, to_date
    )
    current_candle_index = 300
    ohlc = candle_data[0 : current_candle_index - 1]

    while current_candle_index < len(candle_data):
        ohlc.append(candle_data[current_candle_index])
        entry.enter(exchange, symbol, ohlc)
        exit.exit(exchange, symbol, ohlc)
        current_candle_index += 1
        print(f"Completed {current_candle_index} out of {len(candle_data)} candles...")


def get_historical_data_for_back_testing(exchange, symbol, from_date, to_date):
    instrument_token = kite_utils.get_symbol_ltp(exchange, symbol)["instrument_token"]

    start_date = dt(from_date.year, from_date.month, from_date.day, 0, 0)

    end_date = start_date + timedelta(days=98)

    historical_data = []

    while end_date <= to_date:
        historical_data.extend(
            kite.historical_data(
                instrument_token,
                from_date=start_date,
                to_date=end_date,
                interval="5minute",
            )
        )
        start_date = end_date
        end_date += timedelta(days=98)

    if end_date > to_date:
        historical_data.extend(
            kite.historical_data(
                instrument_token,
                from_date=start_date,
                to_date=to_date,
                interval="5minute",
            )
        )
    print(historical_data[:5])
    print(f"Historical data fetched... for: {from_date} to {to_date}")

    return historical_data


if __name__ == "__main__":
    strategy_name = "ema_20_close_trend_2009_to_2014"
    pd.DataFrame(list(mongodb.MongoDB.trade_collection.find({}))).to_csv(
        "./analysis/" + strategy_name + ".csv"
    )
    start_back_testing(
        from_date=dt(2014, 1, 1),
        to_date=dt(2015, 12, 31),
    )

    pd.DataFrame(list(mongodb.MongoDB.trade_collection.find({}))).to_csv(
        "./analysis/" + strategy_name + ".csv"
    )
