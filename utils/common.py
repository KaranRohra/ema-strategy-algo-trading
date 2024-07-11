from datetime import datetime


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


def get_risk_managed_qty(entry_price, stoploss, risk_amount):
    return risk_amount // abs(entry_price - stoploss)
