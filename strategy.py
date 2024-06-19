import ta.trend as trend
import pandas as pd
from utils.common import last

from pytrendseries import detecttrend as pydt
from connection import kite


def _cnt_above_below(left_key: str, right_key: str, ohlc: list):
    cnt = 0
    for i in range(len(ohlc) - 1, -1, -1):
        if ohlc[i][left_key] <= ohlc[i][right_key]:
            break
        cnt += 1
    return cnt


def _strategy(ohlc: list):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_close_above_ema50": 0,
        "candle_cnt_close_below_ema50": 0,
        "candle_cnt_ema50_above_ema200": 0,
        "candle_cnt_ema50_below_ema200": 0,
        "signal": None,
        "date": str(curr["date"]),
    }

    analysis["candle_cnt_close_above_ema50"] = _cnt_above_below("close", "ema50", ohlc)
    analysis["candle_cnt_close_below_ema50"] = _cnt_above_below("ema50", "close", ohlc)
    analysis["candle_cnt_ema50_above_ema200"] = _cnt_above_below("ema50", "ema200", ohlc)
    analysis["candle_cnt_ema50_below_ema200"] = _cnt_above_below("ema200", "ema50", ohlc)

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
    price_trend = pydt(
        pd.DataFrame({"price": price}), trend=trend, limit=5, window=1000
    ).to_dict(orient="records")
    return {
        f"is_{param_key}_in_{trend}": len(price) - 1 == last(price_trend)["index_to"],
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
    ema20 = trend.ema_indicator(close_series, window=20).tolist()[-1]
    ema200 = trend.ema_indicator(close_series, window=200).tolist()[-1]

    return (
        kite.TRANSACTION_TYPE_SELL if ema20 < ema200 else kite.TRANSACTION_TYPE_BUY
    )
