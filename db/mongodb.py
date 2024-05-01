import pymongo
import os

from constants import Env


class MongoDB:
    _client = pymongo.MongoClient(os.environ.get(Env.MONGO_URI))
    _db = _client[os.environ.get(Env.MONGO_DB)]
    trade_collection = _db["trades"]
    holding_collection = _db["holdings"]
    candle_collection = _db["candles"]

    holding_cache = None
