import ta.trend
import pandas as pd

from constants import Signal
from kite import utils as kite_utils


def get_stoploss(exchange, symbol):
    return round(
        ta.trend.ema_indicator(
            close=pd.Series(
                [h["close"] for h in kite_utils.get_historical_data(exchange, symbol)]
            ),
            window=200,
        ).to_list()[-1]
    )


def is_ema_crossed(close):
    close_series = pd.Series(close)
    ema200 = ta.trend.ema_indicator(close=close_series, window=200).to_list()

    return {
        "is_close_above_ema200": close[-1] > ema200[-1],
        "is_close_below_ema200": close[-1] < ema200[-1],
    }


def exit_signal(exchange, symbol):
    close = [h["close"] for h in kite_utils.get_historical_data(exchange, symbol)]
    analyzed_params = is_ema_crossed(close)

    if analyzed_params["is_close_below_ema200"]:
        return Signal.EXIT_LONG_POSITION

    if analyzed_params["is_close_above_ema200"]:
        return Signal.EXIT_SHORT_POSITION
