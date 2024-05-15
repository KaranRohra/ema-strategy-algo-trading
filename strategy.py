import ta.trend as trend
import pandas as pd
import utils

from pytrendseries import detecttrend as dt
from constants import kite


def _strategy(ohlc: list):
    curr, n = ohlc[-1], len(ohlc)
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_close_above_ema50": 0,
        "candle_cnt_close_below_ema50": 0,
        "candle_cnt_ema50_above_ema200": 0,
        "candle_cnt_ema50_below_ema200": 0,
        "signal": None,
    }

    for i in range(n - 1, -1, -1):
        if ohlc[i]["close"] <= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_above_ema50"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["close"] >= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_below_ema50"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema50"] <= ohlc[i]["ema200"]:
            break
        analysis["candle_cnt_ema50_above_ema200"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema50"] >= ohlc[i]["ema200"]:
            break
        analysis["candle_cnt_ema50_below_ema200"] += 1

    if (
        analysis["close_above_emas"]
        and analysis["is_ema20_in_uptrend"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_BUY

    if (
        analysis["close_below_emas"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_SELL

    return analysis


def get_trend_analysis(price, trend, param_key):
    price_trend = dt(pd.DataFrame({"price": price}), trend=trend).to_dict(
        orient="records"
    )
    return {
        f"is_{param_key}_in_{trend}": len(price) - 1
        == utils.last(price_trend)["index_to"],
    }


def get_entry_signal(ohlc: list):
    close = [c["close"] for c in ohlc]
    close_series = pd.Series(close)
    ema20 = trend.ema_indicator(close_series, window=20).tolist()
    ema50 = trend.ema_indicator(close_series, window=50).tolist()
    ema200 = trend.ema_indicator(close_series, window=200).tolist()

    ohlc[-1].update(
        {
            **get_trend_analysis(ema20, "uptrend", "ema20"),
            **get_trend_analysis(ema50, "uptrend", "ema50"),
            **get_trend_analysis(ema200, "uptrend", "ema200"),
            **get_trend_analysis(ema20, "downtrend", "ema20"),
            **get_trend_analysis(ema50, "downtrend", "ema50"),
            **get_trend_analysis(ema200, "downtrend", "ema200"),
        }
    )

    i = -1
    while i >= -len(ohlc):
        if i >= -len(ema20):
            ohlc[i]["ema20"] = ema20[i]
        if i >= -len(ema50):
            ohlc[i]["ema50"] = ema50[i]
        if i >= -len(ema200):
            ohlc[i]["ema200"] = ema200[i]
        i -= 1

    return _strategy(ohlc)


def get_exit_signal(ohlc: list):
    close = [c["close"] for c in ohlc]
    close_series = pd.Series(close)
    ema200 = trend.ema_indicator(close_series, window=200).tolist()[-1]

    return (
        kite.TRANSACTION_TYPE_SELL if close[-1] < ema200 else kite.TRANSACTION_TYPE_BUY
    )
