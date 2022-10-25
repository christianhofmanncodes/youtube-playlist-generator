"""module strings.replace_string"""


def replace_space_in_string(string: str) -> str:
    """
    The replace_space_in_string function replaces spaces in a string with %20.

    :param string:str: Used to Specify the string that is to be modified.
    :return: A string with the spaces replaced by %20.
    """
    return string.replace(" ", "%20")


def create_comma_separated_string(content_list: list) -> str:
    """
    The create_comma_separated_string function takes a list of strings
    and returns a string with all the items separated by commas.

    :param content_list:list: Used to Pass the list that is going to be converted into a string.
    :return: A string with commas after each item from the list.
    """
    return ",".join(content_list)
