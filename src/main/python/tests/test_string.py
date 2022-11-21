"""module tests.test_string"""

from strings import check_string, replace_string


def test_replace_string() -> None:
    """
    The test_replace_string function tests the replace_space_in_string function.
    It passes a string to the function and checks
    if it returns a modified version of that string.

    :return: A string with any kind of space replaced by "%20".
    """
    string = "This is a test string."
    assert (
        replace_string.replace_space_in_string(string)
        == "This%20is%20a%20test%20string."
    )


def test_create_comma_separated_string() -> None:
    """
    The test_create_comma_separated_string function
    tests the create_comma_separated_string function.
    It does this by creating a list of strings
    and then checking if the output is what it should be.

    :return: A comma-separated string created from the content_list.
    """
    content_list = ["item1", "item2", "item3"]
    assert (
        replace_string.create_comma_separated_string(content_list)
        == "item1,item2,item3"
    )


def test_remove_empty_strings_in_list() -> None:
    """
    The test_remove_empty_strings_in_list function
    tests the remove_empty_strings_in_list function.
    It passes a list of strings to the function
    and expects a list with no empty strings in return.

    :return: A list with the empty strings removed.
    """
    list_of_strings = ["", "item1", "item2", "", "item3", ""]
    assert replace_string.remove_empty_strings_in_list(list_of_strings) == []


def test_format_int_with_commas() -> None:
    """
    The test_format_int_with_commas function
    tests the format_int_with_commas function.
    It passes a number to the function
    and checks that it is formatted correctly.

    :return: "10,345,236".
    """
    number = 10345236
    assert replace_string.format_int_with_commas(number) == "10,345,236"


def test_has_space_in_string() -> None:
    """
    The test_has_space_in_string function tests the has_space_in_string function.
    It passes a string with spaces and checks if the function returns True.

    :return: True if space in string, otherwise False.
    """
    string = "There is no space in string."
    assert check_string.has_space_in_string(string) is True
