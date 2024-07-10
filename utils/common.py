import traceback

from datetime import datetime
from mail import app as ma


def first(lst: list):
    return lst[0] if lst else None


def last(lst: list):
    return lst[-1] if lst else None


def title_to_snake(input_string: str) -> str:
    snake_case_string = input_string.replace(" ", "_").lower()
    return snake_case_string


def time_str_to_curr_datetime(time_string: str) -> datetime:
    now = datetime.now()
    return datetime.strptime(time_string, "%H:%M:%S").replace(
        year=now.year, month=now.month, day=now.day
    )


def notify_error_details(e):
    error_details = {"type": type(e).__name__, "message": str(e)}
    traceback_details = traceback.format_exc()
    subject = f"Error Report: {error_details['type']} in your script"
    ma.send_error_email(subject, error_details, traceback_details)
