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

# print(kite.profile())
# # print(kite.basket_order_margins())
res = requests.get(
    "https://kite.zerodha.com/api/baskets",
    headers={
        "Accept": "application/json",
        # "Accept-Encoding": "gzip, deflate, br, zstd",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Cookie": "kf_session=qdl8cb5DiFCHaWr283xzv4EZX9zbs5AQ; user_id=AXN756; _cfuvid=_nTA8hvcpeNdnYxjuZkAWxTez_.9.S13RKDO3U2HZw8-1716565266552-0.0.1.1-604800000; public_token=uoMKz5NrFpEHA7cMcCNba2aRhtCUOayG; enctoken=24PBNv3a1nlp8rOMrTL4C70miTVBNLZkyHsoLmBy+nYQzMIztoRbIPlYiVpeHouxux+pk51VGNQvAkeFKVH0weWbGFwkexS/eipfQGj+oGBxhRs0BMdIsA==; __cf_bm=da.4l5aLy5F8UHQV4Dj9WHhbpO5y0QuDIEoiS3u0fbU-1716663723-1.0.1.1-fCkzFXPl5g57ybC6jKpywt_IvL9RlTk41wVrjNwUXNaJ74GDAVllDEZHEQpay4rHTpfoHQYaX.E1Xxjnl5bjiA",
        "Cookie": "kf_session=FJTJabDtufJXuqlNuo90raAtxHm4Vg76; user_id=AXN756; public_token=uoMKz5NrFpEHA7cMcCNba2aRhtCUOayG; enctoken=F263Fq4ioeC/lp2Vf6S/mqD7jorWyvsOytmAa05KNmhiyW6SRjiS8ltxVWZ2YCkTLkRzQtg7Yq3PYELk05aRtTEJil5sbOv6xJNUZimkLp2OCUlBaQ8HZg==; __cf_bm=0QRVn_NjGvw.P2cfOAHLoIwDdasdVV8pxeC.09AfPN4-1716675275-1.0.1.1-LDSa8qC00x.qiN0BGhVQyy7QPvoPhk9NmRcfuN7KbEJ9VXIYGReGnDYmhSfz2om6DtsY9gkJPbUf2ALV7iSgiA"
        # "Priority": "u=1, i",
        # "Referer": "https://kite.zerodha.com/orders/baskets",
        # "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        # "Sec-Ch-Ua-Mobile": "?0",
        # "Sec-Ch-Ua-Platform": '"Windows"',
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin"
        ,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Csrftoken": "uoMKz5NrFpEHA7cMcCNba2aRhtCUOayG",
        # "X-Kite-App-Uuid": "06c72153-7416-431b-a208-5186e4f1459a",
        # "X-Kite-Userid": "AXN756",
        # "X-Kite-Version": "3.0.0",
    },
)
print(res.json())
