import orders
import schedule
import threading
import time

from mail import app as ma
from datetime import datetime as dt
from gsheet import users as gusers
from gsheet.environ import GOOGLE_SHEET_ENVIRON
from utils import kite_utils as ku, market_utils as mu, common


def scan_users_basket(users):
    GOOGLE_SHEET_ENVIRON.set_environ()
    now = dt.now()
    is_perfect_time_entry = now.minute % GOOGLE_SHEET_ENVIRON.entry_time_frame == 0
    is_perfect_time_exit = now.minute % GOOGLE_SHEET_ENVIRON.exit_time_frame == 0

    symbol_scan = []
    for user in gusers.get_or_update_users(users):
        if not user.active:
            continue

        if now < user.start_time or now > user.end_time:
            continue

        holdings = user.kite.holdings()
        positions = user.kite.positions()
        tokens = []
        for sd in ku.get_basket_items(user.kite, user.basket):

            if sd["instrument_token"] in user.in_process_symbols:
                continue

            holding = ku.get_holding(positions, holdings, sd["instrument_token"])
            ss = {
                "user": user,
                "sd": sd,
            }

            if holding:
                if is_perfect_time_exit:
                    ss["thread"] = threading.Thread(
                        target=orders.search_exit, args=(user, holding)
                    )

            else:
                if is_perfect_time_entry:
                    ss["thread"] = threading.Thread(
                        target=orders.search_entry, args=(user, sd)
                    )
            symbol_scan.append(ss)
            tokens.append(sd["instrument_token"])
        ku.cancel_orders(user.kite, tokens)

    for ss in symbol_scan:
        user: gusers.User = ss["user"]
        thread = ss.get("thread")
        if thread:
            thread.start()

    # Added waiting condition so that other threads can execute faster
    now = dt.now()
    if now.second < 56:
        time.sleep(56 - now.second)


def start():
    GOOGLE_SHEET_ENVIRON.set_environ()
    while mu.is_trading_time():
        try:
            users = gusers.get_or_update_users()
            schedule.every().minute.at(":00").do(scan_users_basket, users)
            while mu.is_trading_time():
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            print(f"[{dt.now()}]: {e}")
            ma.send_error_email(e)
            time.sleep(5)
        GOOGLE_SHEET_ENVIRON.set_environ()
