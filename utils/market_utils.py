from datetime import datetime as dt
from os import environ
from constants import Env


def is_market_open() -> bool:
    now = dt.now()
    TIME_FORMAT = "%H:%M:%S"
    start_time = dt.strptime(environ[Env.START_TIME], TIME_FORMAT)
    start_time = start_time.replace(year=now.year, month=now.month, day=now.day)

    end_time = dt.strptime(environ[Env.END_TIME], TIME_FORMAT)
    end_time = end_time.replace(year=now.year, month=now.month, day=now.day)

    market_open = start_time <= now <= end_time
    if not market_open:
        print(f"Market is closed: {now} - Market timings: {start_time} - {end_time}")
    return market_open


def get_candle_interval(time_frame) -> str:
    return {
        "1": "minute",
        "day": "day",
        "3": "3minute",
        "5": "5minute",
        "10": "10minute",
        "15": "15minute",
        "30": "30minute",
        "60": "60minute",
    }[time_frame]
