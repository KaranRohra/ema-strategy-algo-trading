import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect
from dhanhq import dhanhq

load_dotenv()

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


# Broker Connect Objects
kite = KiteConnect(api_key=f"enctoken {os.getenv('KITE_API_KEY')}")
