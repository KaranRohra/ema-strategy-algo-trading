import pymongo
import os

from constants import Env


class MongoDB:
    os.environ[Env.MONGO_DB] = "prod"
    _client = pymongo.MongoClient(os.environ.get(Env.MONGO_URI))
    _db = _client[os.environ.get(Env.MONGO_DB)]
    trades = _db["trades"]
    holdings = _db["holdings"]
    candles = _db["candles"]
    holidays = _db["holidays"]
