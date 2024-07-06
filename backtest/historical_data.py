from utils import kite_utils as ku
import os, time
from constants import Env
from connection import kite
from datetime import datetime as dt, timedelta as td
import pandas as pd
import pandas_ta as pta
from ta import trend
from pytrendseries import detecttrend as pydt


def get_historical_data(from_date, to_date, instrument_token):
    start_date = from_date
    end_date = start_date + td(days=90)
    ohlc = []

    while end_date < to_date:
        data = kite.historical_data(instrument_token, start_date, end_date, "5minute")
        ohlc.extend(data)

        if len(ohlc):
            print(f"Fetched data for: {start_date} - {end_date}")

        start_date = end_date + td(days=1)
        end_date = start_date + td(days=90)
        # time.sleep(1)

    return ohlc


def get_trend_analysis(price, trend):
    res = set()
    trend_analysis = [
        range(t["index_from"], t["index_to"])
        for t in pydt(
            pd.DataFrame({"price": price}), trend=trend, limit=5, window=1000
        ).to_dict(orient="records")
    ]

    for r in trend_analysis:
        res.update(list(r))
    return res

def add_indicator_values(ohlc: list):
    for p in ohlc:
        p["date"] = str(p["date"])
    print("Started Adding Indicators")
    ohlc_df = pd.DataFrame(ohlc)
    close_series = ohlc_df["close"]
    print("Started Adding Indicators")
    ema20 = pta.ema(close_series, length=20).tolist()
    ema50 = pta.ema(close_series, length=50).tolist()
    ema200 = pta.ema(close_series, length=200).tolist()
    print("Calculated EMAs")
    supertrend_dir = [
        s["SUPERTd_10_3.0"]
        for s in pta.supertrend(
            high=ohlc_df["high"],
            low=ohlc_df["low"],
            close=ohlc_df["close"],
            length=10,
            multiplier=3,
        ).to_dict("records")
    ]
    print("Calculated ST")

    ema20_uptrend = get_trend_analysis(ema20, "uptrend")
    print("Calculated EMA 20")
    ema50_uptrend = get_trend_analysis(ema50, "uptrend")
    print("Calculated EMA 50")
    ema200_uptrend = get_trend_analysis(ema200, "uptrend")
    print("Calculated EMA 200")
    ema20_downtrend = get_trend_analysis(ema20, "downtrend")
    print("Calculated EMA 20")
    ema50_downtrend = get_trend_analysis(ema50, "downtrend")
    print("Calculated EMA 50")
    ema200_downtrend = get_trend_analysis(ema200, "downtrend")
    print("Calculated EMA 200")

    for i in range(len(ohlc)):
        p = ohlc[i]
        p["ema20"] = ema20[i]
        p["ema50"] = ema50[i]
        p["ema200"] = ema200[i]

        p["supertrend_dir"] = supertrend_dir[i]
        p["is_ema20_in_uptrend"] = i in ema20_uptrend
        p["is_ema50_in_uptrend"] = i in ema50_uptrend
        p["is_ema200_in_uptrend"] = i in ema200_uptrend

        p["is_ema20_in_downtrend"] = i in ema20_downtrend
        p["is_ema50_in_downtrend"] = i in ema50_downtrend
        p["is_ema200_in_downtrend"] = i in ema200_downtrend
    
    pd.DataFrame(ohlc).to_csv("./analysis/nifty50/final_candle_analysis.csv")


def backtest():
    from_date = dt(2015, 1, 1)
    to_date = dt.now()
    ohlc = get_historical_data(from_date, to_date, 256265)
    add_indicator_values(ohlc)


backtest()
