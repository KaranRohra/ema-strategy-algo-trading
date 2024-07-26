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
    while True:
        try:
            GOOGLE_SHEET_ENVIRON.set_environ()
            trading.start()
            break
        except Exception as e:
            print(f"[{dt.now()}]: {e}")
            ma.send_error_email(e)
            time.sleep(5)

    print(f"[{dt.now()}] Trading Stopped")
    ma.send_trading_stop_email()
