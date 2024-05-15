import pymongo

from os import environ
from constants import Env


class MongoDB:
    _client = pymongo.MongoClient(environ[Env.MONGO_URI])
    _db = _client[environ[Env.MONGO_DB]]
    trades = _db["trades"]
    holdings = _db["holdings"]
