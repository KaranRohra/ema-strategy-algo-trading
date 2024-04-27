import os
import pandas as pd
import utils

from dotenv import load_dotenv
from constants import CANDLE_CSV_PATH, Holding, Trade
from strategy.entry import get_analyzed_params
from orders import orders
from kite_utils import kite_utils
from datetime import datetime as dt


load_dotenv()


def dump_candle_data(exchange, symbol):
    candle_details = (
        os.path.exists(CANDLE_CSV_PATH)
        and pd.read_csv(CANDLE_CSV_PATH).to_dict(orient="records")
        or []
    )
    close = [h["close"] for h in kite_utils.get_historical_data(exchange, symbol)]
    candle_details.append(get_analyzed_params(close))

    pd.DataFrame(candle_details).to_csv(CANDLE_CSV_PATH, index=False)


def dump_holding_data(entry_details):
    holding_df = pd.read_csv(Holding.CSV_PATH)
    holding_details = holding_df.to_dict(orient="records")
    holding_details.append(entry_details)
    pd.DataFrame(holding_details, columns=holding_df.columns).to_csv(
        Holding.CSV_PATH, index=False
    )


def dump_trade_data(exit_details):
    trades_df = pd.read_csv(Trade.CSV_PATH)
    holding_df = pd.read_csv(Holding.CSV_PATH)

    holding_details = holding_df.to_dict(orient="records")
    trade_details = trades_df.to_dict(orient="records")

    holding_details = [
        h for h in holding_details if h[Holding.SYMBOL] != exit_details[Trade.SYMBOL]
    ]
    trade_details.append(exit_details)

    pd.DataFrame(trade_details, columns=trades_df.columns).to_csv(
        Trade.CSV_PATH, index=False
    )
    pd.DataFrame(holding_details, columns=holding_df.columns).to_csv(
        Holding.CSV_PATH, index=False
    )


def start_trading():
    symbol = os.environ["SYMBOL"]
    exchange = os.environ["EXCHANGE"]

    while utils.is_trading_time():

        if not utils.is_market_open():
            continue

        now = dt.now()
        if now.minute % 5 == 0 and now.second == 0:
            if kite_utils.is_symbol_in_holdings_or_position(symbol):
                exit_details = orders.exit_order(exchange, symbol)
                if exit_details:
                    dump_trade_data(exit_details)
            else:
                entry_details = orders.entry_order(exchange, symbol)
                if entry_details:
                    dump_holding_data(entry_details)

            dump_candle_data(exchange, symbol)
            print(now.strftime("%Y-%m-%d %H:%M:%S") + " - Candle data dumped...")
    else:
        print("Trading time is between 9:15 AM to 3:30 PM. Exiting...")
