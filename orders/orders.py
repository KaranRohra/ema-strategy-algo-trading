from constants import Signal, Holding, kite, Trade
from strategy import entry, exit
from datetime import datetime as dt
from kite_utils import kite_utils


def entry_order(exchange, symbol):
    signal = entry.entry_signal(exchange, symbol)
    exchange_symbol = f"{exchange}:{symbol}"
    ohlc = kite.ohlc([exchange_symbol])[exchange_symbol]["ohlc"]
    if kite_utils.get_holding(symbol):
        return None

    entry_details = {
        Holding.SYMBOL: symbol,
        Holding.DATETIME: dt.now(),
        Holding.STOPLOSS: exit.get_stoploss(exchange, symbol),
    }

    if signal == Signal.ENTER_LONG_POSITION:
        entry_details[Holding.TRANSACTION_TYPE] = kite.TRANSACTION_TYPE_BUY
        entry_details[Holding.PRICE] = ohlc["high"]

        return entry_details
    elif signal == Signal.ENTER_SHORT_POSITION:
        entry_details[Holding.TRANSACTION_TYPE] = kite.TRANSACTION_TYPE_SELL
        entry_details[Holding.PRICE] = ohlc["low"]

        return entry_details


def exit_order(exchange, symbol):
    signal = exit.exit_signal(exchange, symbol)

    holding = kite_utils.get_holding(symbol)
    exchange_symbol = f"{exchange}:{symbol}"
    if holding is None:
        return None

    exit_details = {
        Trade.SYMBOL: holding[Holding.SYMBOL],
        Trade.FROM: holding[Holding.DATETIME],
        Trade.TO: dt.now(),
        Trade.ENTRY_PRICE: holding[Holding.PRICE],
        Trade.EXIT_PRICE: kite.ltp(exchange_symbol)[exchange_symbol]["last_price"],
        Trade.TRANSACTION_TYPE: holding[Holding.TRANSACTION_TYPE],
        Trade.STOPLOSS: holding[Holding.STOPLOSS],
    }

    if (
        holding[Holding.TRANSACTION_TYPE] == kite.TRANSACTION_TYPE_BUY
        and signal == Signal.EXIT_LONG_POSITION
    ):
        exit_details[Trade.P_AND_L] = round(
            exit_details[Trade.EXIT_PRICE] - exit_details[Trade.ENTRY_PRICE]
        )

        return exit_details
    elif (
        holding[Holding.TRANSACTION_TYPE] == kite.TRANSACTION_TYPE_SELL
        and signal == Signal.EXIT_SHORT_POSITION
    ):
        exit_details[Trade.P_AND_L] = round(
            exit_details[Trade.ENTRY_PRICE] - exit_details[Trade.EXIT_PRICE]
        )

        return exit_details
