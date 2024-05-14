import ta.trend as trend
import pandas as pd
from pytrendseries import detecttrend as pydt


def get_trend_analysis(price, trend, param_key):
    price_trend = pydt(
        pd.DataFrame({"price": price}),
        trend=trend,
    ).to_dict(orient="records")

    if len(price_trend) == 0:
        return {
            f"is_{param_key}_in_{trend}": False,
            f"{param_key}_{trend}_time_span": 0,
        }

    price_trend = price_trend[-1]

    is_in_trend = len(price) - 1 == price_trend["index_to"]

    return {
        f"is_{param_key}_in_{trend}": is_in_trend,
        f"{param_key}_{trend}_time_span": (
            price_trend["time_span"] if is_in_trend else 0
        ),
    }


def get_analyzed_params(ohlc, trend_type) -> dict:
    close = [c["close"] for c in ohlc]
    close_series = pd.Series(close)
    ema20 = trend.ema_indicator(close_series, window=20).tolist()
    ema50 = trend.ema_indicator(close_series, window=50).tolist()
    ema100 = trend.ema_indicator(close_series, window=100).tolist()
    ema200 = trend.ema_indicator(close_series, window=200).tolist()

    candle_cnt_above_ema50 = 0
    candle_cnt_below_ema50 = 0
    for i in range(len(close) - 1, -1, -1):
        if close[i] <= ema50[i]:
            break
        candle_cnt_above_ema50 += 1

    for i in range(len(close) - 1, -1, -1):
        if close[i] >= ema50[i]:
            break
        candle_cnt_below_ema50 += 1
    return {
        "close_above_emas": close[-1] > ema50[-1] > ema200[-1],
        "close_below_emas": close[-1] < ema50[-1] < ema200[-1],
        "candle_cnt_above_ema50": candle_cnt_above_ema50,
        "candle_cnt_below_ema50": candle_cnt_below_ema50,
        **get_trend_analysis(close, trend_type, "close"),
        # **get_trend_analysis(ema20, trend_type, "ema20"),
        **get_trend_analysis(ema50, trend_type, "ema50"),
        # **get_trend_analysis(ema100, trend_type, "ema100"),
        # **get_trend_analysis(ema200, trend_type, "ema200"),
    }


def can_enter_long_position(ohlc):
    analyzed_params = get_analyzed_params(ohlc, "uptrend")

    return (
        analyzed_params["is_close_in_uptrend"]
        and analyzed_params["is_ema20_in_uptrend"]
        and analyzed_params["is_ema50_in_uptrend"]
        and analyzed_params["is_ema100_in_uptrend"]
    )


def can_enter_short_position(ohlc):
    analyzed_params = get_analyzed_params(ohlc, "downtrend")

    return (
        analyzed_params["is_close_in_downtrend"]
        and analyzed_params["is_ema20_in_downtrend"]
        and analyzed_params["is_ema50_in_downtrend"]
        and analyzed_params["is_ema100_in_downtrend"]
        and analyzed_params["is_ema200_in_downtrend"]
    )


def can_exit_long_position(ohlc):
    close = [c["close"] for c in ohlc]
    ema200 = trend.ema_indicator(pd.Series(close), window=200).tolist()
    return close[-1] < ema200[-1]


def can_exit_short_position(ohlc):
    close = [c["close"] for c in ohlc]
    ema200 = trend.ema_indicator(pd.Series(close), window=200).tolist()
    return close[-1] > ema200[-1]
