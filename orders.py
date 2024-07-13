import strategy
import time

from typing import List
from utils import kite_utils as ku, common
from datetime import datetime as dt, timedelta as td
from mail import app as mail_app
from gsheet.users import User
from gsheet.environ import GOOGLE_SHEET_ENVIRON


def place_entry_order(user: User, order_details, holding, instrument_token):
    kite = user.kite
    exchange, symbol = holding["exchange"], holding["symbol"]
    tran_type = order_details["transaction_type"]
    now = dt.now()
    wait_time = GOOGLE_SHEET_ENVIRON.entry_time_frame * 2.8
    end_minutes = (wait_time * 10) // 10
    end_seconds = (wait_time * 10) % 10
    wait_seconds = end_minutes * 60
    valid_till = now + td(minutes=end_minutes, seconds=end_seconds)
    print(
        f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: Waiting for High/Low Break"
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
        print(f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: {msg}")
        return

    # Don't take trade if loss is higher than risk_amount
    risk_qty = common.get_risk_managed_qty(
        order_details["price"], holding["ema200"], user.risk_amount
    )
    if risk_qty < holding["quantity"]:
        print(
            f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: Risk is higher than Risk Amount"
        )
        return
    order_id = kite.place_order(**order_details)
    msg = "Order placed successfully"
    details = {"order_id": order_id, **holding}
    print(f"[{dt.now()}] [{user.user_id}] [{exchange}:{symbol}]: {msg}")
    mail_app.send_order_status_email(details, msg)


def search_entry(user: User, symbol_details):
    kite = user.kite
    symbol, exchange = symbol_details["tradingsymbol"], symbol_details["exchange"]
    instrument_token = symbol_details["instrument_token"]
    ohlc = ku.get_historical_data(
        kite, instrument_token, GOOGLE_SHEET_ENVIRON.entry_time_frame
    )

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

    place_entry_order(user, order_detail, holding, instrument_token)
    user.in_process_symbols.remove(instrument_token)


def search_exit(user: User, holding):
    kite = user.kite
    ohlc = ku.get_historical_data(
        kite, holding["instrument_token"], GOOGLE_SHEET_ENVIRON.exit_time_frame
    )
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
    if ku.get_order_status(kite, str(order_id))["status"] == kite.STATUS_COMPLETE:
        msg = "Order executed successfully"
    else:
        msg = "Order failed"
    print(
        f"[{dt.now()}] [{user.user_id}] [{holding['exchange']}:{holding['tradingsymbol']}]: {msg}"
    )
    mail_app.send_order_status_email(details, msg)


def cancel_basket_scripts_orders(user: User, instrument_tokens: List[int]):
    kite = user.kite
    for o in kite.orders():
        if o["instrument_token"] in (instrument_tokens) and o["status"] not in (
            kite.STATUS_COMPLETE,
            kite.STATUS_CANCELLED,
            kite.STATUS_REJECTED,
        ):
            kite.cancel_order(o["variety"], o["order_id"])
