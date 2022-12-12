from datetime import datetime

from django.test import TestCase


def calculate_age(birth_date):
    today = datetime.date.today()
    try:
        birthday = birth_date.replace(year=today.year)

    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = birth_date.replace(year=today.year,
                                      month=birth_date.month + 1, day=1)

    if birthday > today:
        age = today.year - birth_date.year - 1
        return str(age)
    else:
        age = today.year - birth_date.year
        return str(age)
