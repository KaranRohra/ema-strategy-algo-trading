import os
import dotenv

from kite.connect import KiteConnect

dotenv.load_dotenv()

kite = KiteConnect(
    headers={
        "Authorization": f"enctoken {os.environ['KITE_API_KEY']}",
        "X-Csrftoken": os.environ["KITE_PUBLIC_TOKEN"],
        "Cookie": os.environ["KITE_COOKIE"],
    }
)


class Env:
    MONGO_URI = "MONGO_URI"
    MONGO_DB = "MONGO_DB"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
    TIME_FRAME = "TIME_FRAME"
