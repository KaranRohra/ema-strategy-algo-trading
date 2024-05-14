import datetime as dt

from constants import kite
from db.mongodb import MongoDB


def get_instrument_token(exchange, symbol):
    return kite.ltp(f"{exchange}:{symbol}")[f"{exchange}:{symbol}"]["instrument_token"]


def get_current_ohlc(exchange, symbol):
    return kite.ohlc(f"{exchange}:{symbol}")[f"{exchange}:{symbol}"]["ohlc"]


def get_symbol_holding(symbol, live=True):
    if live:
        positions = [p for p in kite.positions()["net"] if p["quantity"] != 0]
        positions.extend(kite.holdings())
        symbol_position = [p for p in positions if p["tradingsymbol"] == symbol]
    else:
        symbol_position = list(MongoDB.holdings.find({}))
    return symbol_position[0] if symbol_position else None


def get_historical_data(
    exchange,
    symbol,
    interval="5minute",
    from_date=dt.datetime.now() - dt.timedelta(days=95),
    to_date=dt.datetime.now(),
):
    return kite.historical_data(
        instrument_token=get_instrument_token(exchange, symbol),
        interval=interval,
        from_date=from_date,
        to_date=to_date,
        # continuous=True,
    )


def get_exit_price_for_long_position(exchange, symbol):
    quote = kite.quote(f"{exchange}:{symbol}")[f"{exchange}:{symbol}"]
    depth = quote["depth"]["sell"]
    ltp = quote["last_price"]
    lower_circuit = quote["lower_circuit_limit"]
    for d in depth:
        if d["quantity"] > 0:
            price = d["price"] - 0.05
            if price < lower_circuit:
                return lower_circuit
            return price

    return ltp - 0.05


def get_exit_price_for_short_position(exchange, symbol):
    quote = kite.quote(f"{exchange}:{symbol}")[f"{exchange}:{symbol}"]
    depth = quote["depth"]["buy"]
    ltp = quote["last_price"]
    upper_circuit = quote["upper_circuit_limit"]
    for d in depth:
        if d["quantity"] > 0:
            price = d["price"] + 0.05
            if price > upper_circuit:
                return upper_circuit
            return price

    return ltp + 0.05
