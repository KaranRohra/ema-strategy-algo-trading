import os

from kiteconnect import KiteConnect
from dhanhq import dhanhq

# Candle Analysis
CANDLE_CSV_PATH = "./analysis/candles/"


# Holdings CSV Columns
# symbol,entry_datetime,entry,transaction_type,stoploss
HOLDINGS_CSV_PATH = "./analysis/Holdings.csv"
HOLDING_SYMBOL = "Symbol"
HOLDING_ENTRY_DATETIME = "Entry Datetime"
HOLDING_ENTRY_PRICE = "Price"
HOLDING_TRANSACTION_TYPE = "Transaction Type"
HOLDING_STOPLOSS = "Stoploss"


# Trades CSV Columns
# symbol,trade_from,trade_to,entry,exit,transaction_type,p&l,stoploss
TRADES_CSV_PATH = "./analysis/Trades.csv"
TRADE_SYMBOL = "Symbol"
TRADE_FROM = "From"
TRADE_TO = "To"
TRADE_ENTRY_PRICE = "Entry Price"
TRADE_EXIT_PRICE = "Exit Price"
TRADE_TRANSACTION_TYPE = "Transaction Type"
TRADE_P_AND_L = "P&L"
TRADE_STOPLOSS = "Stoploss"


# ENV Constants Name
KITE_API_KEY = "KITE_API_KEY"
DHAN_ACCESS_TOKEN = "DHAN_ACCESS_TOKEN"
DHAN_CLIENT_ID = "DHAN_CLIENT_ID"
ANGEL_ONE_API_KEY = "ANGEL_ONE_API_KEY"
ANGEL_ONE_SECRET_KEY = "ANGEL_ONE_SECRET_KEY"


# Broker Connect Objects
kite = KiteConnect(api_key=f"enctoken {os.environ[KITE_API_KEY]}")
dhan = dhanhq(os.environ[DHAN_ACCESS_TOKEN], os.environ[DHAN_CLIENT_ID])
