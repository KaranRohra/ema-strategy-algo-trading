import os

from dotenv import load_dotenv
from kite.connect import KiteConnect

load_dotenv()

kite = KiteConnect(api_key=f"enctoken {os.getenv('KITE_API_KEY')}")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Env:
    KITE_API_KEY = "KITE_API_KEY"
    ENV = "ENV"
    SYMBOL = "SYMBOL"
    EXCHANGE = "EXCHANGE"
    MONGO_DB = "MONGO_DB"
    MONGO_URI = "MONGO_URI"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    EMAIL_PASSWORD = "EMAIL_PASSWORD"
    EMAIL_RECIPIENTS = "EMAIL_RECIPIENTS"


class Holding:
    SYMBOL = "symbol"
    DATETIME = "entry_datetime"
    PRICE = "entry_price"
    TRANSACTION_TYPE = "transaction_type"
    STOPLOSS = "stoploss"
    EXCHANGE = "exchange"


class Trade:
    SYMBOL = "symbol"
    FROM = "from"
    TO = "to"
    ENTRY_PRICE = "entry_price"
    EXIT_PRICE = "exit_price"
    ORDER_TRANSACTION_TYPE = "order_transaction_type"
    HOLDING_TRANSACTION_TYPE = "holding_transaction_type"
    P_AND_L = "profit_and_loss"
    STOPLOSS = "stoploss"
    EXCHANGE = "exchange"


class Signal:
    ENTER_LONG_POSITION = "Enter Long Position"
    ENTER_SHORT_POSITION = "Enter Short Position"
    EXIT_LONG_POSITION = "Exit Long Position"
    EXIT_SHORT_POSITION = "Exit Short Position"
