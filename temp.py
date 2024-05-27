import ta.trend as trend, os
import pandas as pd
from datetime import datetime as dt, timedelta as td
from constants import kite
import requests
import json
from utils import kite_utils
from pytrendseries import detecttrend

from backtest.backtest import get_historical_data_for_back_testing
import requests


def dump_historical_data():
    hd = get_historical_data_for_back_testing(
        256265, dt(2015, 1, 1), dt.now(), "5minute"
    )

    for i in range(len(hd)):
        hd[i]["date"] = str(hd[i]["date"])

    pd.DataFrame(hd).to_csv(
        "./analysis/nifty50/candles.csv",
        index=False,
    )


def val_in_range(lst, index):
    for l in lst:
        if l["index_from"] >= index and l["index_to"] <= index:
            return True
    return False


def combine_ema_data():
    ema_20 = pd.read_csv("./analysis/nifty50/ema_20_analysis.csv").to_dict("records")
    ema_50 = pd.read_csv("./analysis/nifty50/ema_50_analysis.csv").to_dict("records")
    ema_200 = pd.read_csv("./analysis/nifty50/ema_200_analysis.csv").to_dict("records")
    candles = pd.read_csv("./analysis/nifty50/candles.csv").to_dict("records")

    hd = []
    for i in range(len(candles)):
        hd.append({**candles[i], **ema_20[i], **ema_50[i], **ema_200[i]})
        print("Completed", i, len(candles))

    pd.DataFrame(hd).to_csv("./analysis/nifty50/final_candle_analysis.csv", index=False)


def dump_ema_analysis_data(ema_value):
    ema_key = f"ema{ema_value}"
    hd = pd.read_csv("./analysis/nifty50/candles.csv").to_dict("records")
    close = [h["close"] for h in hd]
    ema = trend.ema_indicator(pd.Series(close), ema_value)
    ema_uptrend = detecttrend(pd.DataFrame({"price": ema}), trend="uptrend").to_dict(
        "records"
    )
    ema_downtrend = detecttrend(
        pd.DataFrame({"price": ema}), trend="downtrend"
    ).to_dict("records")

    ema_up_set = set()
    for i in range(len(ema_uptrend)):
        ema_up_set.update(
            set(range(ema_uptrend[i]["index_from"], ema_uptrend[i]["index_to"] + 1))
        )

    ema_down_set = set()
    for i in range(len(ema_downtrend)):
        ema_down_set.update(
            set(range(ema_downtrend[i]["index_from"], ema_downtrend[i]["index_to"] + 1))
        )

    # ema_up_set =
    for i in range(len(hd)):
        hd[i][ema_key] = ema[i]
        hd[i][f"is_{ema_key}_in_uptrend"] = i in ema_up_set
        hd[i][f"is_{ema_key}_in_downtrend"] = i in ema_down_set
        print("Completed", i, len(hd))

    pd.DataFrame(hd).to_csv(f"./analysis/nifty50/{ema_key}_analysis.csv", index=False)


# combine_ema_data()
# # print([*[1, 3], *[2, 3, 4]])

