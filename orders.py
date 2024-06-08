import strategy
import time

from utils import kite_utils
from constants import LogType
from connection import kite
from db import MongoDB


def place_entry_order(order_details, holding, instrument_token):
    tran_type = order_details["transaction_type"]
    wait_time = 9 * 60
    while wait_time > 0:
        ohlc = kite_utils.get_ohlc(instrument_token)
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
        time.sleep(1)
        wait_time -= 1
    if wait_time == 0:
        MongoDB.insert_log(
            log_type=LogType.FAIL,
            message="Order failed",
            details={"status": "Candle high/low not break", **holding},
        )
        return
    order_details["validity_ttl"] = wait_time // 60 + 1
    order_id = kite.place_order(**order_details)
    MongoDB.insert_log(
        log_type=LogType.SUCCESS,
        message="Order placed successfully",
        details={"order_id": order_id, **holding},
    )

    while kite_utils.get_order_status(order_id)["status"] not in (
        kite.STATUS_COMPLETE,
        kite.STATUS_REJECTED,
        kite.STATUS_CANCELLED,
    ):
        time.sleep(10)

    if kite_utils.get_order_status(order_id)["status"] == kite.STATUS_COMPLETE:
        MongoDB.holdings.insert_one(holding)
        MongoDB.insert_log(
            log_type=LogType.SUCCESS,
            message="Order executed successfully",
            details={"order_id": order_id, **holding},
        )
    else:
        MongoDB.insert_log(
            log_type=LogType.FAIL,
            message="Order failed",
            details={"order_id": order_id, **holding},
        )


def search_entry(ohlc):
    symbol_details = kite_utils.get_basket_item()
    symbol, exchange = symbol_details["tradingsymbol"], symbol_details["exchange"]
    signal_details = strategy.get_entry_signal(ohlc)
    MongoDB.insert_log(
        log_type=LogType.TRADE,
        message="Searching for entry",
        details={"symbol": symbol, "exchange": exchange, **signal_details},
    )
    if not signal_details["signal"]:
        return

    holding = {
        "symbol": symbol,
        "exchange": exchange,
        "from": ohlc[-1]["date"],
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
        "validity": kite.VALIDITY_TTL,
    }

    place_entry_order(order_detail, holding, symbol_details["instrument_token"])


def search_exit(ohlc, holding):
    signal = strategy.get_exit_signal(ohlc)
    MongoDB.insert_log(
        log_type=LogType.TRADE,
        message="Searching for exit",
        details={
            "symbol": holding["tradingsymbol"],
            "exchange": holding["exchange"],
            "quantity": holding["quantity"],
            "exit_signal": signal,
        },
    )
    MongoDB.holdings.update_many(
        {"symbol": holding["tradingsymbol"]}, {"$set": {"ltp": ohlc[-1]["close"]}}
    )
    if not signal:
        return
    if (
        signal == kite.TRANSACTION_TYPE_BUY and holding["quantity"] > 0
    ):  # If we have bought and signal is to exit buy position
        return
    if (
        signal == kite.TRANSACTION_TYPE_SELL and holding["quantity"] < 0
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

    holding["to"] = ohlc[-1]["date"]

    if kite_utils.get_order_status(str(order_id))["status"] == kite.STATUS_COMPLETE:
        entry_signal_details = MongoDB.holdings.find_one(
            {"symbol": holding["tradingsymbol"]}
        )
        holding.update(entry_signal_details)
        MongoDB.holdings.delete_one({"symbol": holding["tradingsymbol"]})
        MongoDB.trades.insert_one(holding)
        MongoDB.insert_log(
            log_type=LogType.SUCCESS,
            message="Order executed successfully",
            details={"order_id": order_id, **holding},
        )
    else:
        MongoDB.insert_log(
            log_type=LogType.FAIL,
            message="Order failed",
            details={"order_id": order_id, **holding},
        )
