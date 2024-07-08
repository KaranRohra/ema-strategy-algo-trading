import dotenv

dotenv.load_dotenv()

import trading
import time
import os
import pyotp
import traceback

from constants import Env, LogType
from connection import kite
from db import MongoDB
from mail import app as ma


def notify_error_details(e):
    error_details = {"type": type(e).__name__, "message": str(e)}
    traceback_details = traceback.format_exc()
    subject = f"Error Report: {error_details['type']} in your script"
    MongoDB.insert_log(log_type=LogType.ERROR, message=subject, details=traceback_details)
    ma.send_error_email(subject, error_details, traceback_details)


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
            kite.reconnect(two_fa=pyotp.TOTP(os.environ[Env.KITE_2FA_SECRET]).now())
            notify_error_details(e)
            error_caught = True

    MongoDB.insert_log(log_type=LogType.INFO, message="Trading stopped")
    ma.send_trading_stop_email()
