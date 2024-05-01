import time
import os

from strategy.start_trading import start_trading
from constants import Env
from mail.app import Mail


os.environ["TZ"] = "Asia/Kolkata"
if os.environ[Env.ENV] == "PROD":
    time.tzset()


if __name__ == "__main__":
    try:
        start_trading()
    except Exception as e:
        print(e)
        Mail.send_error_email(str(e))
