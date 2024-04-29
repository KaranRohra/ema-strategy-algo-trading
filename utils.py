import math
import os

from datetime import datetime, time
from holidays import HOLIDAYS


def get_market_status():
    now = datetime.now()
    open_time = time(9, 0)
    close_time = time(15, 30)

    holiday = [h for h in HOLIDAYS if now.strftime("%d %b %Y") == h["Date"]]

    if now.weekday() == 5 or now.weekday() == 6:
        return {"open": False, "reason": "Weekend"}
    if len(holiday):
        return {"open": False, "reason": holiday[0]["Holiday"]}

    now_time = now.time()
    open = now_time >= open_time and now_time <= close_time
    if open:
        reason = "Market is open now..."
    else:
        reason = f"Market timing is 9:00 AM to 3:30 PM - Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    return {"open": open, reason: reason}


def is_trading_time():
    now = datetime.now().time()
    start_time = time(9, 15, 0)
    end_time = time(15, 29, 30)

    return now >= start_time and now <= end_time


def get_qty(entry, stoploss, available_capital):
    risk_amount = os.environ.get("RISK_AMOUNT", 1000)
    qty = math.abs(risk_amount // (entry - stoploss))
    required_capital = qty * entry

    if required_capital >= available_capital:
        return available_capital // entry

    return qty
