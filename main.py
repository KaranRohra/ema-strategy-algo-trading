import time
import os
from strategy.start_trading import start_trading


os.environ["TZ"] = "Asia/Kolkata"
if os.environ["ENV"] == "PROD":
    time.tzset()


if __name__ == "__main__":
    start_trading()
