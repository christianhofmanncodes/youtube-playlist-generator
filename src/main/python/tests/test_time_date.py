"""module tests.test_time_date"""

from datetime import datetime

from time_and_date import convert_date, convert_time


def test_format_date() -> None:
    """
    The test_format_date function tests the format_date function.
    It passes a datetime object to the format_date function
    and checks that it returns a string in the correct format.

    :return: "yyyy-mm-dd".
    """
    dt = datetime(2022, 11, 22)
    assert convert_date.format_date(dt) == "2022-11-22"


def test_convert_hours_minutes_seconds() -> None:
    """
    The test_convert_hours_minutes_seconds function
    tests the convert_hours_minutes_seconds function.
    It does this by checking that the correct output is produced for a given input.

    :return: "hh:mm:ss".
    """
    seconds = 3600
    assert convert_time.convert_hours_minutes_seconds(seconds) == "01:00:00"
