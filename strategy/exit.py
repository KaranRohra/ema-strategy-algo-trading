import ta.trend
import pandas as pd

from constants import Trade, Holding, kite
from kite import utils as kite_utils
from db.mongodb import MongoDB


def is_ema_crossed(close):
    close_series = pd.Series(close)
    ema200 = ta.trend.ema_indicator(close=close_series, window=200).to_list()

    return {
        "is_close_above_ema200": close[-1] > ema200[-1],
        "is_close_below_ema200": close[-1] < ema200[-1],
    }


def exit(exchange, symbol, ohlc):
    close = [candle["close"] for candle in ohlc]
    analyzed_params = is_ema_crossed(close)
    holding = kite_utils.get_holding(symbol)
    if holding is None:
        return

    exit_details = {
        **holding,
        Trade.FROM: holding[Holding.DATETIME],
        Trade.TO: ohlc[-1]["date"],
        Trade.ENTRY_PRICE: holding[Holding.PRICE],
        Trade.EXIT_PRICE: ohlc[-1]["close"],
    }

    if (
        analyzed_params["is_close_below_ema200"]
        and holding[Holding.TRANSACTION_TYPE] == kite.TRANSACTION_TYPE_BUY
    ) or (
        analyzed_params["is_close_above_ema200"]
        and holding[Holding.TRANSACTION_TYPE] == kite.TRANSACTION_TYPE_SELL
    ):
        MongoDB.trade_collection.insert_one(exit_details)
        MongoDB.holding_collection.delete_one({Holding.SYMBOL: symbol})
        print(f"Exited Position for {symbol} at {ohlc[-1]['date']}...")
