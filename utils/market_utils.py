from datetime import datetime as dt
from os import environ
from constants import Env


def is_trading_time() -> bool:
    now = dt.now()
    TIME_FORMAT = "%H:%M:%S"
    start_time = dt.strptime(environ[Env.START_TIME], TIME_FORMAT)
    start_time = start_time.replace(year=now.year, month=now.month, day=now.day)

    end_time = dt.strptime(environ[Env.END_TIME], TIME_FORMAT)
    end_time = end_time.replace(year=now.year, month=now.month, day=now.day)

    return start_time <= now <= end_time
