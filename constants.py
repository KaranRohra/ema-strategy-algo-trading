import os

from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()


# Holdings CSV Columns
# symbol,entry_datetime,entry,transaction_type,stoploss
class Holding:
  SYMBOL = "symbol"
  DATETIME = "entry_datetime"
  PRICE = "price"
  TRANSACTION_TYPE = "transaction_type"
  STOPLOSS = "stoploss"

# Trades CSV Columns
# symbol,trade_from,trade_to,entry,exit,transaction_type,p&l,stoploss
class Trade:
  SYMBOL = "symbol"
  FROM = "from"
  TO = "to"
  ENTRY_PRICE = "entry_price"
  EXIT_PRICE = "exit_price"
  TRANSACTION_TYPE = "transaction_type"
  P_AND_L = "profit_and_loss"
  STOPLOSS = "stoploss"


# Strategy Constants
class Signal:
  ENTER_LONG_POSITION = "Enter Long Position"
  ENTER_SHORT_POSITION = "Enter Short Position"
  EXIT_LONG_POSITION = "Exit Long Position"
  EXIT_SHORT_POSITION = "Exit Short Position"

# Broker Connect Objects
kite = KiteConnect(api_key=f"enctoken {os.getenv('KITE_API_KEY')}")
