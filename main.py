import pandas as pd
import time
import os

import constants
from datetime import datetime
from utils import utils
from order_placement import order_placement as op
from strategy import strategy


def start_trading():
    candle_csv_name = (
        constants.CANDLE_CSV_PATH + (datetime.now()).strftime("%d-%m-%Y") + ".csv"
    )
    candle_details = (
        os.path.exists(candle_csv_name)
        and pd.read_csv(candle_csv_name).to_dict(orient="records")
        or []
    )

    while True:
        if utils.is_market_open():
            now = datetime.now()
            # if now.minute % 5 == 0 and now.second == 2:
            if utils.is_symbol_in_holdings_or_position():
                op.exit()
                candle_details.append(strategy.get_scanning_result())
            else:
                candle_details.append(op.enter())
            pd.DataFrame(candle_details).to_csv(candle_csv_name, index=False)
            time.sleep(2)
        else:
            print(
                f"Current Time: {datetime.now()} ******* Market is closed now....",
                end="\r",
            )


if __name__ == "__main__":
    start_trading()
