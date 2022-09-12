"""module strings.check_string"""


def is_string_valid_url(string: str) -> bool:
    """Check if http:// or https:// in string and return bool value."""
    return "http://" in string or "https://" in string


def is_string_valid_youtube_url(string: str) -> bool:
    """Check if watch? or be/ in string and return bool value."""
    return "watch?" in string or "be/" in string


def has_space_in_string(string: str) -> bool:
    """Return True if space in string."""
    return " " in string
