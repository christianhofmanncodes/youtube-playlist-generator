"""module strings.replace_string"""


def replace_space_in_string(string: str) -> str:
    """Return string with spaces replaced by %20."""
    return string.replace(" ", "%20")


def create_comma_separated_string(content_list: list) -> str:
    """Add commas after each item from list and return it as a string."""
    return ",".join(content_list)
