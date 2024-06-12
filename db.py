import pymongo

from os import environ
from constants import Env
from datetime import datetime as dt


class MongoDB:
    _client = pymongo.MongoClient(environ[Env.MONGO_URI])
    _db = _client[environ[Env.MONGO_DB]]
    trades = _db["trades"]
    holdings = _db["holdings"]
    logs = _db["logs"]

    @staticmethod
    def insert_log(log_type, message, details={}):
        MongoDB.logs.insert_one(
            {
                "timestamp": str(dt.now()),
                "logType": log_type,
                "message": message,
                "details": details,
            }
        )
