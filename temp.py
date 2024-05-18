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

print(kite.profile())
print(kite.login_url())
