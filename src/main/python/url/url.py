"""module url.url"""


def cut_url_to_id(url: str) -> str:
    """Return id from video URL."""
    if "v=" in url:
        get_id = url.split("v=")
    elif "be/" in url:
        get_id = url.split("be/")
    return get_id[-1]


def create_playlist_url(video_ids: str, playlist_title: str, with_title: bool) -> str:
    """Create playlist URL with a title from video ids and title, if title given."""
    if with_title:
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"
    return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"
