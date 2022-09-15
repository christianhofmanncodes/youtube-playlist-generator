"""module strings.check_string"""


def is_string_valid_url(string: str) -> bool:
    """
    The is_string_valid_url function checks if the string contains http:// or https://.
    If it does, then it returns True, otherwise False.

    :param string:str: Used to Pass the string that will be checked.
    :return: A boolean value of true if the string contains http:// or https://.
    """
    return "http://" in string or "https://" in string


def is_string_valid_youtube_url(string: str) -> bool:
    """
    The is_string_valid_youtube_url function checks if the string contains either "watch?" or "be/" in it.
    If it does, then the function returns True, otherwise False.

    :param string:str: Used to Pass a string value to the function.
    :return: A boolean value.
    """
    return "watch?" in string or "be/" in string


def has_space_in_string(string: str) -> bool:
    """
    The has_space_in_string function returns True if a space is in the string passed to it.

    :param string:str: Used to Tell the function that it will be receiving a string.
    :return: True if the string contains a space.
    """
    return " " in string
