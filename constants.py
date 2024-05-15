import os

from kite.connect import KiteConnect

kite = KiteConnect(api_key=f"enctoken {os.environ['KITE_API_KEY']}")


class Env:
    SYMBOL = "SYMBOL"
    EXCHANGE = "EXCHANGE"
    SEGMENT = "SEGMENT"
    QUANTITY = "QUANTITY"
    LOT_SIZE = "LOT_SIZE"
    MONGO_URI = "MONGO_URI"
    MONGO_DB = "MONGO_DB"
