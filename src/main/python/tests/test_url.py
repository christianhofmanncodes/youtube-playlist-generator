"""tests.test_url module"""
from main import Ui


def test_is_string_valid_url() -> None:
    """Test Ui.is_string_valid_url()"""
    url_string = "https://youtube-playlist-generator.com"
    youtube_url_string = "https://invidious.namazso.eu/watch?v=gQlMMD8auMs"
    assert Ui.is_string_valid_url(Ui, url_string) is True
    assert Ui.is_string_valid_youtube_url(Ui, youtube_url_string) is True


def test_create_playlist_url() -> None:
    """Test Ui.test_create_playlist_url()"""
    video_ids = "gQlMMD8auMs,dYRITmpFbJ4"
    playlist_title = "K-Pop"
    assert (
        Ui.create_playlist_url_without_title(Ui, video_ids)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4"
    )
    assert (
        Ui.create_playlist_url_with_title(Ui, video_ids, playlist_title)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4&title=K-Pop"
    )
