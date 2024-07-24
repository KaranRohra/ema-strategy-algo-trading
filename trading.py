import orders
import schedule
import threading
import time

from mail import app as ma
from datetime import datetime as dt
from gsheet import users as gusers
from gsheet.environ import GOOGLE_SHEET_ENVIRON
from utils import kite_utils as ku, market_utils as mu


def search_trade(
    user: gusers.User, holding, symbol_details, trade_signal
):
    token = symbol_details["instrument_token"]
    user.in_process_symbols.add(token)
    try:
        if trade_signal == "ENTRY":
            orders.search_entry(user, symbol_details)
        elif trade_signal == "EXIT":
            orders.search_exit(user, holding)
    except Exception as e:
        print(
            f"[{dt.now()}] [{user.user_id}] [{symbol_details['exchange']}:{symbol_details['tradingsymbol']}]: {trade_signal}",
        )
        ma.send_error_email(e)
    finally:
        user.in_process_symbols.discard(token)


def scan_single_user(
    user: gusers.User, now: dt, is_perfect_time_entry: bool, is_perfect_time_exit: bool
):
    if not user.active:
        return

    if now < user.start_time or now > user.end_time:
        return

    holdings = user.kite.holdings()
    positions = user.kite.positions()
    tokens = []
    basket_items = ku.get_basket_items(user, user.basket)
    for sd in basket_items:
        tokens.append(sd["instrument_token"])

    # Canceling all orders before scanning the scripts
    orders.cancel_basket_scripts_orders(user, tokens)

    for sd in basket_items:

        if sd["instrument_token"] in user.in_process_symbols:
            continue

        holding = ku.get_holding(positions, holdings, sd["instrument_token"])
        TRADE_SIGNAL = None
        if holding:
            if is_perfect_time_exit:
                TRADE_SIGNAL = "EXIT"
        else:
            if is_perfect_time_entry:
                TRADE_SIGNAL = "ENTRY"
        if TRADE_SIGNAL:
            threading.Thread(
                target=search_trade,
                args=(user, holding, sd, TRADE_SIGNAL),
                name=f"[{dt.now()}] [{user.user_id}] [{sd['exchange']}:{sd['tradingsymbol']}]: {TRADE_SIGNAL}",
            ).start()


def scan_users_basket(users):
    GOOGLE_SHEET_ENVIRON.set_environ()
    now = dt.now()
    is_perfect_time_entry = now.minute % GOOGLE_SHEET_ENVIRON.entry_time_frame == 0
    is_perfect_time_exit = now.minute % GOOGLE_SHEET_ENVIRON.exit_time_frame == 0

    for user in gusers.get_or_update_users(users):
        try:
            scan_single_user(user, now, is_perfect_time_entry, is_perfect_time_exit)
        except Exception as e:
            print(f"[{dt.now()}]: {e}")
            user.set_kite_obj()
            ma.send_error_email(e)

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
            GOOGLE_SHEET_ENVIRON.set_environ()
            time.sleep(5)
