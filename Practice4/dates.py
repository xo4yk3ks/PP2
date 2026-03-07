
from datetime import datetime, timedelta


def current_datetime():
    return datetime.now()


def add_days(date, days):
    return date + timedelta(days=days)


def days_between(date1, date2):
    return abs((date2 - date1).days)

