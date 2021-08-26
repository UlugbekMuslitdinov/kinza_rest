import datetime


def phone_validator(phone):
    if phone.startswith('+998'):
        if len(phone) == 13:
            return True
        if len(phone) == 17 and '-' in phone:
            return True
    else:
        return False


def date_validator(date):
    """Validates a date string in DD-MM-YYYY format"""
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError:
        return False