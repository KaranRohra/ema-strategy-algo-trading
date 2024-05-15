from os import environ
from utils import KiteUtils
from constants import Env
import ta.trend as trend
import pandas as pd

exchange, symbol = environ[Env.EXCHANGE], environ[Env.SYMBOL]
ohlc = KiteUtils.get_historical_data(exchange, symbol)

print(trend.ema_indicator(pd.Series([x["close"] for x in ohlc]), 200).tolist()[-1])
# 'ema200': 86515.8163505018
