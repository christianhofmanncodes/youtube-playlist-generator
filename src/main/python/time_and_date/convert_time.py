"""module time_and_date.time"""

import time


def convert_hours_minutes_seconds(seconds: int) -> str:
    """
    The convert_seconds_hours_minutes function converts seconds to hours, minutes and seconds.
    It takes in a number of seconds as an argument and returns
    the equivalent number of hours, minutes and seconds.

    :param self: Used to Access the class attributes.
    :param seconds:int: Used to Pass the number
           of seconds to be converted into hours, minutes and seconds.
    :return: A string that represents the time in hours, minutes and seconds.
    """
    ty_res = time.gmtime(seconds)
    return time.strftime("%H:%M:%S", ty_res)
