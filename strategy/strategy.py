import pandas as pd
import pytrendseries

from ta import trend
from datetime import datetime

from constants import *
from config import *

from kite_utils.kite_utils import *


def is_close_gt_or_lt_20_50_100_200_ema(dir="gt"):  # dir -> gt or lt
    historical_data = get_historical_data()

    close = [h["close"] for h in historical_data]
    ema20 = trend.ema_indicator(close=pd.Series(close), window=20).to_list()[-1]
    ema50 = trend.ema_indicator(close=pd.Series(close), window=50).to_list()[-1]
    ema100 = trend.ema_indicator(close=pd.Series(close), window=100).to_list()[-1]
    ema200 = trend.ema_indicator(close=pd.Series(close), window=200).to_list()[-1]

    return (
        close[-1] > ema20 > ema50 > ema100 > ema200
        if dir == "gt"
        else close[-1] < ema20 < ema50 < ema100 < ema200
    )


def is_in_trend(trend="uptrend"):  # trend -> uptrend or downtrend
    historical_data = get_historical_data()
    close = [h["close"] for h in historical_data][
        len(historical_data) - 60 : len(historical_data)
    ]
    trend_series = pytrendseries.detecttrend(
        pd.DataFrame({"close": close}), trend=trend
    )
    trend_detail = {
        f"is_in_{trend}": len(close) - 1 in trend_series["index_to"].values,
        f"{trend}_time_span": 0,
    }
    if trend_detail[f"is_in_{trend}"]:
        trend_detail[f"{trend}_time_span"] = trend_series["time_span"].values[-1]
    return trend_detail


def is_close_crossed_ema200(dir="lt"):  # dir -> gt or lt
    historical_data = get_historical_data()
    close = [h["close"] for h in historical_data]
    ema200 = trend.ema_indicator(close=pd.Series(close), window=200).to_list()

    return close[-1] < ema200[-1] if dir == "lt" else close[-1] > ema200[-1]


def get_stoploss():
    return round(
        trend.ema_indicator(
            close=pd.Series([h["close"] for h in get_historical_data()]), window=200
        ).to_list()[-1]
    )


def get_entry(transaction_type=kite.TRANSACTION_TYPE_BUY):
    historical_data = get_historical_data()[-1]
    return (
        historical_data["high"]
        if transaction_type == kite.TRANSACTION_TYPE_BUY
        else historical_data["low"]  # SELL
    )


def get_scanning_result():
    return {
        "symbol": SYMBOL,
        "candle_time": datetime.now(),
        "is_close_gt_ema": is_close_gt_or_lt_20_50_100_200_ema("gt"),
        **is_in_trend("uptrend"),
        "is_close_lt_ema": is_close_gt_or_lt_20_50_100_200_ema("lt"),
        **is_in_trend("downtrend"),
    }
