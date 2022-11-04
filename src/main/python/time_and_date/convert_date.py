"""module time_and_date.date"""

from datetime import datetime


def format_date(dt: datetime) -> str:
    """
    The format_date function takes a datetime object
    and returns a string in the format YYYY-MM-DD.

    :param self: Used to Access attributes and methods of the class in which it is used.
    :param dt:datetime: Used to Pass in a datetime object.
    :return: A string in the format yyyy-mm-dd.
    """
    return dt.strftime("%Y-%m-%d")
