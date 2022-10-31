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


def remove_empty_strings_in_list(list_of_strings: list) -> list[str]:
    """
    The remove_empty_strings_in_list function takes a list of strings
    and returns a list without empty strings.

    :param list_of_strings:list: The list of strings to remove empty strings
    :return: A list of strings with empty strings removed
    """
    return [i for i in list_of_strings[0] if i]
