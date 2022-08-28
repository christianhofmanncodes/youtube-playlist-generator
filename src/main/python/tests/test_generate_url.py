from main import Ui


def test_create_playlist_url_without_title() -> None:
    video_ids = "gQlMMD8auMs,dYRITmpFbJ4"
    assert (
        Ui.create_playlist_url_without_title(Ui, video_ids)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4"
    )


def test_create_playlist_url_with_title() -> None:
    video_ids = "gQlMMD8auMs,dYRITmpFbJ4"
    playlist_title = "K-Pop"
    assert (
        Ui.create_playlist_url_with_title(Ui, video_ids, playlist_title)
        == "https://www.youtube.com/watch_videos?video_ids=gQlMMD8auMs,dYRITmpFbJ4&title=K-Pop"
    )
