import pandas as pd
import pytrendseries
import ta.trend

from constants import Signal
from kite import utils as kite_utils
from datetime import datetime as dt


def get_trend_analysis(price, trend):
    return pytrendseries.detecttrend(
        pd.DataFrame({"price": price}),
        trend=trend,
    ).to_dict(orient="records")[-1]


def get_ema5_and_ema20_analysis(ema5, ema20, trend):
    ema20_trend = get_trend_analysis(ema20, trend)
    ema5_trend = get_trend_analysis(ema5, trend)

    ema5_and_ema20_analysis = {
        f"is_ema5_in_{trend}": len(ema5) - 1 == ema5_trend["index_to"],
        f"ema5_{trend}_time_span": 0,
        f"is_ema20_in_{trend}": len(ema20) - 1 == ema20_trend["index_to"]
        and ema20_trend["time_span"] >= 10,
        f"ema20_{trend}_time_span": 0,
    }

    if ema5_and_ema20_analysis[f"is_ema5_in_{trend}"]:
        ema5_and_ema20_analysis[f"ema5_{trend}_time_span"] = ema5_trend["time_span"]

    if ema5_and_ema20_analysis[f"is_ema20_in_{trend}"]:
        ema5_and_ema20_analysis[f"ema20_{trend}_time_span"] = ema20_trend["time_span"]

    return ema5_and_ema20_analysis


def get_analyzed_params(exchange, symbol) -> dict:
    close = [h["close"] for h in kite_utils.get_historical_data(exchange, symbol)]
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
        **get_ema5_and_ema20_analysis(ema5, ema20, "uptrend"),
        "close_below_emas": close[-1] < ema20[-1] < ema50[-1] < ema100[-1] < ema200[-1],
        **get_ema5_and_ema20_analysis(ema5, ema20, "downtrend"),
    }


def entry_signal(exchange, symbol) -> Signal:
    analyzed_params = get_analyzed_params(exchange, symbol)

    if (
        analyzed_params["close_above_emas"]
        and analyzed_params["is_ema5_in_uptrend"]
        and analyzed_params["is_ema20_in_uptrend"]
    ):
        return Signal.ENTER_LONG_POSITION

    if (
        analyzed_params["close_below_emas"]
        and analyzed_params["is_ema5_in_downtrend"]
        and analyzed_params["is_ema20_in_downtrend"]
    ):
        return Signal.ENTER_SHORT_POSITION
