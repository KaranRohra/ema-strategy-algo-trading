import os
import dotenv

from kite.connect import KiteConnect

dotenv.load_dotenv()

kite = KiteConnect(
    user_id=os.environ["KITE_USER_ID"],
    password=os.environ["KITE_PASSWORD"],
    two_fa=os.environ["KITE_TWO_FA"],
)


class Env:
    SYSTEM = "SYSTEM"
    MONGO_URI = "MONGO_URI"
    MONGO_DB = "MONGO_DB"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
    TIME_FRAME = "TIME_FRAME"
