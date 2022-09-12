"""tests.test_url module"""

from strings import check_string
from url import url


def test_is_string_valid_url() -> None:
    """Test check_string.is_string_valid_url()"""
    url_string = "https://youtube-playlist-generator.com"
    youtube_url_string = "https://invidious.namazso.eu/watch?v=gQlMMD8auMs"
    assert check_string.is_string_valid_url(url_string) is True
    assert check_string.is_string_valid_youtube_url(youtube_url_string) is True


def test_create_playlist_url() -> None:
    """Test Ui.test_create_playlist_url()"""
    video_ids = "gQlMMD8auMs,dYRITmpFbJ4"
    playlist_title = "K-Pop"
    assert (
        url.create_playlist_url(video_ids, "", False)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4"
    )
    assert (
        url.create_playlist_url(video_ids, playlist_title, True)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4&title=K-Pop"
    )
