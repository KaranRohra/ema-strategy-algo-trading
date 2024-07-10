import dotenv

dotenv.load_dotenv()
# logging.basicConfig(format="[%(asctime)s]:[%(levelname)s] - %(message)s")

import trading
import time
import os

from constants import Env
from mail import app as ma
from datetime import datetime as dt


os.environ["TZ"] = "Asia/Kolkata"
if os.environ[Env.SYSTEM] == "ubuntu":
    time.tzset()

if __name__ == "__main__":
    trading.start()
    print(f"[{dt.now()}] Trading Stopped")
    ma.send_trading_stop_email()
