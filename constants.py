import os
import dotenv

from kite.connect import KiteConnect

dotenv.load_dotenv()

kite = KiteConnect(api_key=f"enctoken {os.environ['KITE_API_KEY']}")


class Env:
    SYMBOL = "SYMBOL"
    EXCHANGE = "EXCHANGE"
    SEGMENT = "SEGMENT"
    PRODUCT_TYPE = "PRODUCT_TYPE"
    QUANTITY = "QUANTITY"
    LOT_SIZE = "LOT_SIZE"
    MONGO_URI = "MONGO_URI"
    MONGO_DB = "MONGO_DB"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
