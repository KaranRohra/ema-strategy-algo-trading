import strategy
import time

from os import environ
from utils import get_product_type, KiteUtils
from constants import kite, Env
from db import MongoDB


def place_entry_order(exchange, symbol, order_details, holding):
    tran_type = order_details["transaction_type"]
    wait_time = 9 * 60
    while wait_time > 0:
        ltp = KiteUtils.get_ltp(exchange, symbol)
        if tran_type == kite.TRANSACTION_TYPE_BUY and ltp >= order_details["price"]:
            order_details["price"] = ltp
            break
        elif tran_type == kite.TRANSACTION_TYPE_SELL and ltp <= order_details["price"]:
            order_details["price"] = ltp
            break
        time.sleep(1)
        wait_time -= 1
    order_details["validity_ttl"] = wait_time // 60 + 1
    order_id = kite.place_order(**order_details)
    print(f"Order placed: {order_id}")
    while KiteUtils.get_order_status(order_id)["status"] not in (
        kite.STATUS_COMPLETE,
        kite.STATUS_REJECTED,
        kite.STATUS_CANCELLED,
    ):
        time.sleep(10)

    if KiteUtils.get_order_status(order_id)["status"] == kite.STATUS_COMPLETE:
        MongoDB.holdings.insert_one(holding)
    print(f"Order executed: {order_id}")


def search_entry(exchange, symbol, ohlc):
    signal_details = strategy.get_entry_signal(ohlc)
    if not signal_details["signal"]:
        return
    holding = {
        "symbol": symbol,
        "exchange": exchange,
        "quantity": int(environ[Env.QUANTITY]),
        "entry_price": (
            ohlc[-1]["high"]
            if signal_details["signal"] == kite.TRANSACTION_TYPE_BUY
            else ohlc[-1]["low"]
        ),
        "from": ohlc[-1]["date"],
        **signal_details,
    }
    print(f"Signal details: {signal_details}")

    order_detail = {
        "tradingsymbol": symbol,
        "exchange": exchange,
        "product": get_product_type(),
        "variety": kite.VARIETY_REGULAR,
        "transaction_type": signal_details["signal"],
        "quantity": holding["quantity"],
        "order_type": kite.ORDER_TYPE_LIMIT,
        "price": holding["entry_price"],
        "validity": kite.VALIDITY_TTL,
    }

    place_entry_order(exchange, symbol, order_detail, holding)


def search_exit(ohlc, holding):
    signal = strategy.get_exit_signal(ohlc)
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

    if KiteUtils.get_order_status(order_id)["status"] == kite.STATUS_COMPLETE:
        MongoDB.holdings.delete_one({"symbol": holding["tradingsymbol"]})
        MongoDB.trades.insert_one(holding)
        print(f"Order executed successfully: {order_id}")
    else:
        print(f"Order failed: {order_id}")
