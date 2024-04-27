import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect
from datetime import datetime as dt

load_dotenv()

# Candle Analysis
CANDLE_CSV_PATH = f"./analysis/candles/{dt.now().strftime("%d-%m-%Y")}.csv"


# Holdings CSV Columns
# symbol,entry_datetime,entry,transaction_type,stoploss
class Holding:
  CSV_PATH = "./analysis/Holdings.csv"
  SYMBOL = "Symbol"
  DATETIME = "Entry Datetime"
  PRICE = "Price"
  TRANSACTION_TYPE = "Transaction Type"
  STOPLOSS = "Stoploss"

# Trades CSV Columns
# symbol,trade_from,trade_to,entry,exit,transaction_type,p&l,stoploss
class Trade:
  CSV_PATH = "./analysis/Trades.csv"
  SYMBOL = "Symbol"
  FROM = "From"
  TO = "To"
  ENTRY_PRICE = "Entry Price"
  EXIT_PRICE = "Exit Price"
  TRANSACTION_TYPE = "Transaction Type"
  P_AND_L = "P&L"
  STOPLOSS = "Stoploss"


# Strategy Constants
class Signal:
  ENTER_LONG_POSITION = "Enter Long Position"
  ENTER_SHORT_POSITION = "Enter Short Position"
  EXIT_LONG_POSITION = "Exit Long Position"
  EXIT_SHORT_POSITION = "Exit Short Position"

# Broker Connect Objects
kite = KiteConnect(api_key=f"enctoken {os.getenv('KITE_API_KEY')}")
