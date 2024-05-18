import strategy
import time

from os import environ
from utils import get_product_type, KiteUtils
from constants import kite, Env
from db import MongoDB
from datetime import datetime as dt


def search_entry(exchange, symbol, ohlc):
    signal_details = strategy.get_entry_signal(ohlc)
    order_details = {
        "tradingsymbol": symbol,
        "exchange": exchange,
        "product": get_product_type(),
        "variety": kite.VARIETY_REGULAR,
        "quantity": int(environ[Env.QUANTITY]),
        "order_type": kite.ORDER_TYPE_SLM,
        "validity": kite.VALIDITY_TTL,
        "validity_ttl": 9,
    }
    holding = {
        "symbol": symbol,
        "exchange": exchange,
        "quantity": order_details["quantity"],
        "from": ohlc[-1]["date"],
        **signal_details,
    }
    MongoDB.candles.insert_one(signal_details)
    print(f"Signal details: {signal_details}")
    if signal_details["signal"]:
        order_details["transaction_type"] = signal_details["signal"]
        order_details["trigger_price"] = holding["entry_price"] = (
            ohlc[-1]["high"]
            if signal_details["signal"] == kite.TRANSACTION_TYPE_BUY
            else ohlc[-1]["low"]
        )
        order_id = kite.place_order(**order_details)
        print(f"Order placed: {order_id}")

        order_time = dt.now()
        while order_time.minute + 9 >= dt.now().minute:
            time.sleep(10)
            if KiteUtils.get_order_status(order_id) == kite.STATUS_COMPLETE:
                MongoDB.holdings.insert_one(holding)
                print(f"Order executed successfully: {order_id}")
                return
        print(f"Order cancelled: {order_id}")


def search_exit(ohlc, holding):
    signal = strategy.get_exit_signal(ohlc, holding)
    if not signal:
        return
    order_id = kite.place_order(
        tradingsymbol=holding["tradingsymbol"],
        exchange=holding["exchange"],
        product=get_product_type(),
        variety=kite.VARIETY_REGULAR,
        transaction_type=signal,
        quantity=holding["quantity"],
        order_type=kite.ORDER_TYPE_MARKET,
        validity=kite.VALIDITY_DAY,
    )

    holding["to"] = ohlc[-1]["date"]

    if KiteUtils.get_order_status(order_id) == kite.STATUS_COMPLETE:
        MongoDB.holdings.delete_one({"symbol": holding["tradingsymbol"]})
        MongoDB.trades.insert_one(holding)
        print(f"Order executed successfully: {order_id}")
    else:
        print(f"Order failed: {order_id}")
