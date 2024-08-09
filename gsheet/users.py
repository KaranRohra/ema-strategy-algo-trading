import pyotp
import gspread
import time

from typing import List
from utils.common import title_to_snake, time_str_to_curr_datetime
from gsheet import connection
from kite.connect import KiteConnect
from datetime import datetime as dt
from constants import SheetIndex
from mail import app as ma


class User:
    def __init__(
        self,
        user_name,
        user_id,
        password,
        two_fa,
        active,
        start_time,
        end_time,
        basket,
        risk_amount,
        in_process_symbols=set(),
    ):
        self.user_name: str = user_name
        self.user_id: str = user_id
        self._password: str = password
        self._two_fa: str = two_fa
        self.active: bool = active == "1"
        self.start_time: dt = time_str_to_curr_datetime(start_time)
        self.end_time: dt = time_str_to_curr_datetime(end_time)
        self.basket: str = basket
        self.in_process_symbols: set = in_process_symbols
        self.risk_amount: int = int(risk_amount)

    def set_kite_obj(self):
        now = dt.now()
        while not (now.second > 3 and now.second < 20):
            now = dt.now()
        self.kite: KiteConnect = KiteConnect(
            user_id=self.user_id,
            password=self._password,
            two_fa=pyotp.TOTP(self._two_fa).now(),
        )
        print(f"[{dt.now()}] [{self.user_id}]: Connection established")

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "user_id": self.user_id,
            "active": self.active,
            "start_time": self.start_time.isoformat(),  # Convert datetime to ISO 8601 string
            "end_time": self.end_time.isoformat(),  # Convert datetime to ISO 8601 string
            "basket": self.basket,
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return (
            "{"
            + f"User ID: {self.user_id}, Status: {self.active}, Start Time: {self.start_time}, End Time: {self.end_time}, Basket: {self.basket}, Risk Amount: {self.risk_amount}"
            + "}"
        )


def get_or_update_users(old_users: List[User] | None = None) -> List[User]:
    """Returns a list of users from the google sheet."""
    try:
        worksheet = connection.get_sheet().get_worksheet(SheetIndex.USER)
        values = worksheet.get_all_values()
        headers = [title_to_snake(h) for h in values[0]]

        users: List[User] = []
        for i in range(1, len(values)):
            # Row is incomplete, some values are missing
            if len(values[i]) != len(headers):
                continue
            user = {}
            for j in range(len(headers)):
                user[headers[j]] = values[i][j]

            user_obj = User(**user)
            if old_users:
                user_obj.kite = old_users[i - 1].kite
                old_users[i - 1] = user_obj
            else:
                user_obj.set_kite_obj()
                users.append(user_obj)

        return old_users or users
    except gspread.exceptions.GSpreadException as e:
        print(f"[{dt.now()}] [GOOGLE_SHEET_ERROR]: {e}")
        ma.send_error_email(e)
        return old_users or []
