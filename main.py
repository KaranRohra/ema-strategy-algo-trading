import dotenv

dotenv.load_dotenv()

import trading
import time
import os

from constants import Env
from mail import app as ma
from datetime import datetime as dt
from gsheet.environ import GOOGLE_SHEET_ENVIRON


os.environ["TZ"] = "Asia/Kolkata"
if os.environ[Env.SYSTEM] == "ubuntu":
    time.tzset()

if __name__ == "__main__":
    trading.start()
    print(f"[{dt.now()}] Trading Stopped")
    ma.send_trading_stop_email()
