from datetime import datetime, timedelta
from constants import Holding, kite
from db import mongodb


def get_symbol_ltp(exchange, symbol):
    kite_symbol = f"{exchange}:{symbol}"
    return kite.ltp(kite_symbol)[kite_symbol]


def get_historical_data(exchange, symbol):
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute - now.minute % 5)
    return kite.historical_data(
        instrument_token=get_symbol_ltp(exchange, symbol)["instrument_token"],
        from_date=now - timedelta(days=95),
        to_date=now,
        interval="5minute",
    )


def get_holding(symbol):
    if mongodb.MongoDB.holding_cache is None:
        mongodb.MongoDB.holding_cache = list(mongodb.MongoDB.holding_collection.find())
    holding = [h for h in mongodb.MongoDB.holding_cache if h[Holding.SYMBOL] == symbol]
    return holding[0] if len(holding) else None
