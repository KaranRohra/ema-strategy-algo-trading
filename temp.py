import ta.trend as trend
from os import environ
import pandas as pd
from datetime import datetime, timedelta as td

# from pytrendseries import detecttrend as dt
import requests

from utils import KiteUtils, last
from constants import Env, kite
from utils import get_product_type
from strategy import get_trend_analysis
from kite.connect import KiteConnect

# res = requests.get(url="https://api.kite.trade/gtt/triggers", headers={"Authorization": "token Karan:ROHRA"})
# print(res.json())
# res = requests.get(url="https://api.kite.trade/gtt/triggers", headers={"Authorization": "enctoken IYrjvehR5R+EvIMXw5u//P00JmnzaUkIPaylQWCqOTyB8NX6Vflp1lSXLg7IEJFOGpKa185xiQgZBlQCsamlkiSm+bYccuJLqYG9h4Nq5H+hCJxKMy6bDw=="})
# print(res.json())
# print(kite.get_gtts())
print(KiteUtils.get_order_status("1791720135774461952"))
# to_date = datetime.now()
# to_date = datetime(
#     to_date.year,
#     to_date.month,
#     to_date.day,
#     to_date.hour,
#     to_date.minute - to_date.minute % 5,
# )
# hd = KiteUtils.get_historical_data(exchange, symbol, to_date=to_date)
# close = [c["close"] for c in hd]
# ema20 = trend.ema_indicator(pd.Series(close), window=20).to_list()
# t = dt(pd.DataFrame({"price": ema20}), trend="uptrend")
# t_dic = t.to_dict(orient="records")

# print(hd[-1])
# print("***************")
# print(ema20[-1])
# print("***************")
# print(t_dic[-1])
# print("***************")
# print(t)
# print("***************")
# print(get_trend_analysis(ema20, "uptrend", "ema20"))

