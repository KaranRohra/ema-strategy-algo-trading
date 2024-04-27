import pandas as pd

from datetime import datetime, timedelta
from constants import Holding, kite


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


def is_symbol_in_holdings_or_position(symbol):
    holdings_df = pd.read_csv(Holding.CSV_PATH)
    return holdings_df.size and symbol in holdings_df[Holding.SYMBOL].values


def get_holding(symbol):
    holdings = pd.read_csv(Holding.CSV_PATH).to_dict(orient="records")
    symbol_holding = [h for h in holdings if h[Holding.SYMBOL] == symbol]

    return symbol_holding and symbol_holding[0] or None
