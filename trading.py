import signals
import os

from kite import utils as ktu
from constants import kite


def start():
    exchange, symbol = os.environ["EXCHANGE"], os.environ["SYMBOL"]
    ohlc = ktu.get_historical_data(exchange, symbol)

    if ktu.get_symbol_holding(symbol):
        search_exit(exchange, symbol, ohlc)
    else:
        search_entry(exchange, symbol, ohlc)


def get_product_type():
    if os.environ["SEGMENT"] == "EQ":
        return kite.PRODUCT_CNC
    elif os.environ["SEGMENT"] == "F&O":
        return kite.PRODUCT_NRML


def search_entry(exchange, symbol, ohlc):
    order_details = {
        "tradingsymbol": symbol,
        "exchange": exchange,
        "product": get_product_type(),
        "variety": kite.VARIETY_REGULAR,
        "quantity": os.environ["QUANTITY"] * os.environ["LOT_SIZE"],
        "order_type": kite.ORDER_TYPE_SLM,
        "validity": kite.VALIDITY_DAY,
    }
    if signals.can_enter_long_position(ohlc):
        order_details["trigger_price"] = ohlc[-1]["high"]
        order_details["transaction_type"] = kite.TRANSACTION_TYPE_BUY
        kite.place_order(order_details)
    elif signals.can_enter_short_position(ohlc):
        order_details["trigger_price"] = ohlc[-1]["low"]
        order_details["transaction_type"] = kite.TRANSACTION_TYPE_SELL
        kite.place_order(order_details)


def search_exit(exchange, symbol, ohlc):
    holding = ktu.get_symbol_holding(symbol)
    order_details = {
        "tradingsymbol": holding["tradingsymbol"],
        "exchange": holding["exchange"],
        "product": get_product_type(),
        "variety": kite.VARIETY_REGULAR,
        "quantity": abs(holding["quantity"]),
        "order_type": kite.ORDER_TYPE_MARKET,
        "validity": kite.VALIDITY_DAY,
    }
    if holding["quantity"] > 0 and signals.can_exit_long_position(ohlc):
        order_details["transaction_type"] = kite.TRANSACTION_TYPE_SELL
        kite.place_order(order_details)
    elif holding["quantity"] < 0 and signals.can_exit_short_position(ohlc):
        order_details["transaction_type"] = kite.TRANSACTION_TYPE_BUY
        kite.place_order(order_details)
