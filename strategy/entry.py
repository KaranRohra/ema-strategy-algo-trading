import pandas as pd
import pytrendseries
import ta.trend

from constants import Signal, Holding, kite
from datetime import datetime as dt
from kite import utils as kite_utils
from db.mongodb import MongoDB


def get_stoploss(ohlc):
    return round(
        ta.trend.ema_indicator(
            close=pd.Series([candle["close"] for candle in ohlc]),
            window=200,
        ).to_list()[-1]
    )


def get_trend_analysis(price, trend, param_key):
    price = price[-150:]
    price_trend = pytrendseries.detecttrend(
        pd.DataFrame({"price": price}),
        trend=trend,
    ).to_dict(orient="records")[-1]

    trend_key = f"is_{param_key}_in_{trend}"
    time_span_key = f"{param_key}_{trend}_time_span"

    analyzed_params = {
        trend_key: len(price) - 1 == price_trend["index_to"],
        time_span_key: 0,
    }

    if analyzed_params[trend_key]:
        analyzed_params[time_span_key] = price_trend["time_span"]

    return analyzed_params


def get_analyzed_params(exchange, symbol, ohlc) -> dict:
    close = [candle["close"] for candle in ohlc]
    close_series = pd.Series(close)
    ema5 = ta.trend.ema_indicator(close=close_series, window=5).to_list()
    ema20 = ta.trend.ema_indicator(close=close_series, window=20).to_list()
    ema50 = ta.trend.ema_indicator(close=close_series, window=50).to_list()
    ema100 = ta.trend.ema_indicator(close=close_series, window=100).to_list()
    ema200 = ta.trend.ema_indicator(close=close_series, window=200).to_list()

    return {
        "symbol": symbol,
        "exchange": exchange,
        "datetime": dt.now(),
        "close_above_emas": close[-1] > ema20[-1] > ema50[-1] > ema100[-1] > ema200[-1],
        **get_trend_analysis(close, "uptrend", "close"),
        # **get_trend_analysis(ema5, "uptrend", "ema5"),
        **get_trend_analysis(ema20, "uptrend", "ema20"),
        "close_below_emas": close[-1] < ema20[-1] < ema50[-1] < ema100[-1] < ema200[-1],
        **get_trend_analysis(close, "downtrend", "close"),
        # **get_trend_analysis(ema5, "downtrend", "ema5"),
        **get_trend_analysis(ema20, "downtrend", "ema20"),
    }


def enter(exchange, symbol, ohlc) -> Signal:
    if kite_utils.get_holding(symbol):
        return

    analyzed_params = get_analyzed_params(exchange, symbol, ohlc)
    entry_details = {
        Holding.EXCHANGE: exchange,
        Holding.SYMBOL: symbol,
        Holding.DATETIME: ohlc[-1]["date"],
        Holding.STOPLOSS: get_stoploss(ohlc),
        Holding.PRICE: ohlc[-1]["close"],
        **analyzed_params,
    }

    # Enter Long Position
    if (
        analyzed_params["close_above_emas"]
        and analyzed_params["is_close_in_uptrend"]
        # and analyzed_params["is_ema5_in_uptrend"]
        and analyzed_params["is_ema20_in_uptrend"]
        and analyzed_params["ema20_uptrend_time_span"] >= 10
    ):
        entry_details[Holding.TRANSACTION_TYPE] = kite.TRANSACTION_TYPE_BUY
        MongoDB.holding_collection.insert_one(entry_details)
        print(f"Entered Long Position for {symbol} at {ohlc[-1]['date']}...")

    # Enter Short Position
    if (
        analyzed_params["close_below_emas"]
        and analyzed_params["is_close_in_downtrend"]
        # and analyzed_params["is_ema5_in_downtrend"]
        and analyzed_params["is_ema20_in_downtrend"]
        and analyzed_params["ema20_downtrend_time_span"] >= 10
    ):
        entry_details[Holding.TRANSACTION_TYPE] = kite.TRANSACTION_TYPE_SELL
        MongoDB.holding_collection.insert_one(entry_details)
        print(f"Entered Short Position for {symbol} at {ohlc[-1]['date']}...")


def signal(exchange, symbol):
    
    ...