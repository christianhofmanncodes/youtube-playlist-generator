from main import Ui


def test_is_string_valid_url() -> None:
    string = "https://youtube-playlist-generator.com"
    assert Ui.is_string_valid_url(Ui, string) == True


def test_is_string_valid_youtube_url() -> None:
    string = "https://invidious.namazso.eu/watch?v=gQlMMD8auMs"
    assert Ui.is_string_valid_youtube_url(Ui, string) == True
