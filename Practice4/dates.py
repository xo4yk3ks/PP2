
"""Date and time operations"""

from datetime import datetime, timedelta


def current_datetime():
    return datetime.now()


def add_days(date, days):
    return date + timedelta(days=days)


def days_between(date1, date2):
    return abs((date2 - date1).days)


if __name__ == "__main__":
    now = current_datetime()
    print("Now:", now)

    future = add_days(now, 10)
    print("After 10 days:", future)

    past = now - timedelta(days=5)
    print("Days between:", days_between(past, now))
