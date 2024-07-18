from datetime import datetime as dt
from gsheet.environ import GOOGLE_SHEET_ENVIRON


def is_trading_time() -> bool:
    now = dt.now()
    return GOOGLE_SHEET_ENVIRON.start_time <= now <= GOOGLE_SHEET_ENVIRON.end_time and (
        not GOOGLE_SHEET_ENVIRON.force_stop
    )
