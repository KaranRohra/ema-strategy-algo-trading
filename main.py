import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import dotenv

dotenv.load_dotenv()

import trading
import time
import os
import pyotp

from constants import Env, LogType
from connection import kite
from db import MongoDB
from mail import app as ma


os.environ["TZ"] = "Asia/Kolkata"
if os.environ[Env.SYSTEM] == "ubuntu":
    time.tzset()

if __name__ == "__main__":
    error_caught = True
    for _ in range(5):
        try:
            if error_caught:
                error_caught = False
                trading.start()
        except Exception as e:
            MongoDB.insert_log(log_type=LogType.ERROR, message=str(e))
            kite.reconnect(two_fa=pyotp.TOTP(os.environ[Env.KITE_2FA_SECRET]).now())
            ma.send_error_email(str(e))
            error_caught = True

    MongoDB.insert_log(log_type=LogType.INFO, message="Trading stopped")
    ma.send_trading_stop_email()
