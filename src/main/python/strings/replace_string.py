"""module strings.replace_string"""

from typing import List

def replace_space_in_string(string: str) -> str:
    """
    The replace_space_in_string function replaces spaces in a string with %20.

    :param string:str: Used to Specify the string that is to be modified.
    :return: A string with the spaces replaced by %20.
    """
    return string.replace(" ", "%20")


def create_comma_separated_string(content_list: List) -> str:
    """
    The create_comma_separated_string function takes a list of strings
    and returns a string with all the items separated by commas.

    :param content_list:list: Used to Pass the list that is going to be converted into a string.
    :return: A string with commas after each item from the list.
    """
    return ",".join(content_list)


def remove_empty_strings_in_list(list_of_strings: List) -> List:
    """
    The remove_empty_strings_in_list function takes a list of strings
    and returns a list without empty strings.

    :param list_of_strings:list: The list of strings to remove empty strings
    :return: A list of strings with empty strings removed
    """
    return [i for i in list_of_strings[0] if i]


def format_int_with_commas(number: int) -> str:
    """
    The format_int_with_commas function takes an integer as input and returns a string with the
    number formatted with commas. For example, if the input is 123456789,
    then this function will return "123,456,789".

    :param self: Used to Access variables that belongs to the class.
    :param number:int: Used to Pass the number that will be formatted.
    :return: A string with commas in place of the thousands separator.
    """
    return f"{number:,}"
