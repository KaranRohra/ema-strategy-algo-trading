import strategy
import time
import os

from utils import kite_utils as ku
from constants import Env
from datetime import datetime as dt, timedelta as td
from mail import app as mail_app
from gsheet.users import User
from kite.connect import KiteConnect


def place_entry_order(kite: KiteConnect, order_details, holding, instrument_token):
    profile = kite.profile()
    tran_type = order_details["transaction_type"]
    now = dt.now()
    wait_time = int(os.environ[Env.ENTRY_TIME_FRAME]) * 2.8
    end_minutes = (wait_time * 10) // 10
    end_seconds = (wait_time * 10) % 10
    wait_seconds = end_minutes * 60
    valid_till = now + td(minutes=end_minutes, seconds=end_seconds)
    print(
        f"[{dt.now()}] [{profile['user_id']}] [{holding['exchange']}:{holding['symbol']}]: Waiting for High/Low Break"
    )

    while now < valid_till:
        ohlc = ku.get_ohlc(kite, instrument_token)
        if (
            tran_type == kite.TRANSACTION_TYPE_BUY
            and ohlc["high"] > order_details["price"]
        ):
            order_details["price"] = holding["entry_price"] = ohlc["high"]
            break
        elif (
            tran_type == kite.TRANSACTION_TYPE_SELL
            and ohlc["low"] < order_details["price"]
        ):
            order_details["price"] = holding["entry_price"] = ohlc["low"]
            break
        now = dt.now()
        wait_seconds -= 1
        time.sleep(1)
    if now >= valid_till:
        msg = "Order failed"
        details = {"status": "Candle high/low not break", **holding}
        mail_app.send_order_status_email(details, msg)
        print(f"[{dt.now()}] [{profile['user_id']}]: {msg}")
        return
    order_id = kite.place_order(**order_details)
    msg = "Order placed successfully"
    details = {"order_id": order_id, **holding}
    print(f"[{dt.now()}] [{profile['user_id']}]: {msg}")
    mail_app.send_order_status_email(details, msg)


def search_entry(user: User, symbol_details):
    kite = user.kite
    symbol, exchange = symbol_details["tradingsymbol"], symbol_details["exchange"]
    instrument_token = symbol_details["instrument_token"]
    time_frame = int(os.environ[Env.ENTRY_TIME_FRAME])
    ohlc = ku.get_historical_data(kite, instrument_token, time_frame)

    signal_details = strategy.get_entry_signal(kite, ohlc)
    print(
        f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: Searching for entry - {signal_details}"
    )
    if not signal_details["signal"]:
        return

    user.in_process_symbols.add(instrument_token)
    holding = {
        **user.to_dict(),
        "symbol": symbol,
        "exchange": exchange,
        "from": str(ohlc[-1]["date"]),
        "product": symbol_details["params"]["product"],
        "quantity": symbol_details["params"]["quantity"],
        "ltp": ohlc[-1]["close"],
        **signal_details,
    }
    risk_managed_qty = user.risk_amount // abs(
        holding["ltp"] - signal_details["ema200"]
    )

    # Don't take trade if loss is higher than risk_amount
    if risk_managed_qty < holding["quantity"]:
        print(
            f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: Risk is higher than Risk Amount"
        )
        return

    if signal_details["signal"] == kite.TRANSACTION_TYPE_BUY:
        holding["entry_price"] = ohlc[-1]["high"]
    else:
        holding["entry_price"] = ohlc[-1]["low"]

    order_detail = {
        "tradingsymbol": symbol,
        "exchange": exchange,
        "product": holding["product"],
        "variety": kite.VARIETY_REGULAR,
        "transaction_type": signal_details["signal"],
        "quantity": holding["quantity"],
        "order_type": kite.ORDER_TYPE_LIMIT,
        "price": holding["entry_price"],
    }

    place_entry_order(kite, order_detail, holding, instrument_token)
    user.in_process_symbols.remove(instrument_token)


def search_exit(user: User, holding):
    kite = user.kite
    time_frame = int(os.environ[Env.EXIT_TIME_FRAME])
    ohlc = ku.get_historical_data(kite, holding["instrument_token"], time_frame)
    signal = strategy.get_exit_signal(kite, ohlc)
    print(
        f"[{dt.now()}] [{user.user_id}] [{holding['exchange']}:{holding['tradingsymbol']}]: Searching for exit - {signal}"
    )
    if not signal:
        return
    if (
        signal == kite.TRANSACTION_TYPE_BUY and holding["quantity"] >= 0
    ):  # If we have bought and signal is to exit buy position
        return
    if (
        signal == kite.TRANSACTION_TYPE_SELL and holding["quantity"] <= 0
    ):  # If we have sold and signal is to exit sell position
        return

    order_id = kite.place_order(
        tradingsymbol=holding["tradingsymbol"],
        exchange=holding["exchange"],
        product=holding["product"],
        variety=kite.VARIETY_REGULAR,
        transaction_type=signal,
        quantity=abs(holding["quantity"]),
        order_type=kite.ORDER_TYPE_MARKET,
        validity=kite.VALIDITY_DAY,
    )

    holding["to"] = str(ohlc[-1]["date"])

    details = {**user.to_dict(), "order_id": order_id, **holding}
    if ku.get_order_status(str(order_id))["status"] == kite.STATUS_COMPLETE:
        msg = "Order executed successfully"
    else:
        msg = "Order failed"
    print(
        f"[{dt.now()}] [{user.user_id}] [{holding['exchange']}:{holding['tradingsymbol']}]: {msg}"
    )
    mail_app.send_order_status_email(details, msg)
