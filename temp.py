import ta.trend as trend
from os import environ
import pandas as pd
from datetime import datetime, timedelta as td
# from pytrendseries import detecttrend as dt


from utils import KiteUtils
from constants import kite, Env
from utils import get_product_type
from strategy import get_trend_analysis

print(kite.get_gtts())
# symbol, exchange = environ[Env.SYMBOL], environ[Env.EXCHANGE]
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

# # order_details = {
# #   "tradingsymbol": symbol,
# #   "exchange": exchange,
# #   "product": get_product_type(),
# #   "variety": kite.VARIETY_REGULAR,
# #   "quantity": 10,
# #   "order_type": kite.ORDER_TYPE_SLM,
# #   "validity": kite.VALIDITY_DAY,
# #   "transaction_type": kite.TRANSACTION_TYPE_BUY,
# #   "trigger_price": 87400,
# # }
# # o = kite.place_order(**order_details)
# # print(o, type(o))

# kite.cancel_order(variety=kite.VARIETY_REGULAR, order_id="2109")


TIME_FORMAT = "%H:%M:%S"
start_time, end_time = datetime.strptime(
    environ["START_TIME"], TIME_FORMAT
), datetime.strptime(environ["END_TIME"], TIME_FORMAT)

print(type(start_time), type(end_time), start_time, end_time)

