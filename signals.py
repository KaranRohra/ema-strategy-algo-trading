import ta.trend as trend
import pandas as pd
from pytrendseries import detecttrend as pydt
from strategies import s7


def get_trend_analysis(price, trend, param_key, limit: int = 5, window: int = 21):
    price_trend = pydt(
        pd.DataFrame({"price": price}),
        trend=trend,
        limit=limit,
        window=window,
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


def get_entry_signal(ohlc) -> dict:
    close = [c["close"] for c in ohlc]
    close_series = pd.Series(close)
    ema20 = trend.ema_indicator(close_series, window=20).tolist()
    ema50 = trend.ema_indicator(close_series, window=50).tolist()
    ema100 = trend.ema_indicator(close_series, window=100).tolist()
    ema200 = trend.ema_indicator(close_series, window=200).tolist()

    ohlc[-1].update(
        {
            **get_trend_analysis(ema20, "uptrend", "ema20"),
            **get_trend_analysis(ema50, "uptrend", "ema50"),
            **get_trend_analysis(ema200, "uptrend", "ema200"),
            **get_trend_analysis(ema20, "downtrend", "ema20"),
            **get_trend_analysis(ema50, "downtrend", "ema50"),
            **get_trend_analysis(ema100, "downtrend", "ema100"),
        }
    )

    for i in range(len(ema200) - 1, -1, -1):
        ohlc[i].update({"ema20": ema20[i], "ema50": ema50[i], "ema200": ema200[i]})
    return s7(ohlc)


def can_exit_long_position(ohlc):
    close = [c["close"] for c in ohlc]
    ema200 = trend.ema_indicator(pd.Series(close), window=200).tolist()
    return close[-1] < ema200[-1]


def can_exit_short_position(ohlc):
    close = [c["close"] for c in ohlc]
    ema200 = trend.ema_indicator(pd.Series(close), window=200).tolist()
    return close[-1] > ema200[-1]
