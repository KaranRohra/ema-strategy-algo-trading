import orders
import schedule
import threading
import time

from os import environ
from constants import Env
from datetime import datetime as dt
from gsheet import users as gusers
from utils import kite_utils as ku, market_utils as mu, common


def scan_users_basket(users):
    now = dt.now()
    entry_time_frame = int(environ[Env.ENTRY_TIME_FRAME])
    exit_time_frame = int(environ[Env.EXIT_TIME_FRAME])

    is_perfect_time_entry = now.minute % entry_time_frame == 0
    is_perfect_time_exit = now.minute % exit_time_frame == 0

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


def start():
    error_caught = 0
    while error_caught < 5:
        try:
            users = gusers.get_or_update_users()
            schedule.every().minute.at(":00").do(scan_users_basket, users)
            while mu.is_trading_time():
                schedule.run_pending()
                now = dt.now()
                # Added waiting condition so that other threads can execute faster
                if now.second < 55:
                    time.sleep(55 - now.second)
            break
        except Exception as e:
            error_caught += 1
            print(f"[{dt.now()}]: {e}")
            common.notify_error_details(e)
            time.sleep(5)
