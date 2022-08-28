"""tests.test_is_string_valid_url module"""
from main import Ui


def test_is_string_valid_url() -> None:
    """Test Ui.is_string_valid_url()"""
    string = "https://youtube-playlist-generator.com"
    assert Ui.is_string_valid_url(Ui, string) is True


def test_is_string_valid_youtube_url() -> None:
    """Test Ui.is_string_valid_youtube_url()"""
    string = "https://invidious.namazso.eu/watch?v=gQlMMD8auMs"
    assert Ui.is_string_valid_youtube_url(Ui, string) is True
