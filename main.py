import dotenv

dotenv.load_dotenv()

import trading
import time
import os

from constants import Env



os.environ["TZ"] = "Asia/Kolkata"
if os.environ[Env.SYSTEM] == "ubuntu":
    time.tzset()

if __name__ == "__main__":
    trading.start()
