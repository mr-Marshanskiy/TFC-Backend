from datetime import datetime, date


def get_now():
    now = datetime.now().astimezone()
    return now


def get_today():
    today = date.today()
    return today


def datetime_iso_to_str(date):
    try:
        date = date.strftime('%d.%m.%Y %H:%M')
    except TypeError as e:
        pass
    return str(date)


def get_time(date):
    try:
        date = date.strftime('%H:%M')
    except TypeError as e:
        pass
    return str(date)