import pymongo
import os


class MongoDB:
    _client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
    _db = _client[os.environ.get("MONGO_DB")]
    trade_collection = _db["trades"]
    holding_collection = _db["holdings"]
    candle_collection = _db["candles"]
