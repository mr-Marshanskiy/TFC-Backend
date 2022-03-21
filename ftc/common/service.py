from datetime import datetime, date

MONTH_LIST = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
DAYS_LIST = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница',
              'Суббота', 'Воскресенье']
DAYS_SHORT_LIST = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

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


def get_short_date(date):
    try:
        date = date.strftime('%d.%m.%Y')
    except TypeError as e:
        pass
    return str(date)


def get_date_ru(datetime):
    try:
        day = datetime.day
        month = MONTH_LIST[datetime.month]
        year = datetime.year
        return f'{day} {month} {year}'
    except TypeError as e:
        return str(datetime)


def get_week_day_ru_full(datetime):
    try:
        return f'{DAYS_LIST[datetime.isoweekday()]}'
    except TypeError as e:
        return str(datetime)


def get_week_day_ru_short(datetime):
    try:
        return f'{DAYS_SHORT_LIST[datetime.isoweekday()]}'
    except TypeError as e:
        return str(datetime)
