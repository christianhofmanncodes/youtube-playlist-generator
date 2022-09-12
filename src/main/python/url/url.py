"""module url.url"""


def cut_url_to_id(url: str) -> str:
    """Return id from video URL."""
    if "v=" in url:
        get_id = url.split("v=")
    elif "be/" in url:
        get_id = url.split("be/")
    return get_id[-1]


def create_playlist_url_with_title(video_ids: str, playlist_title: str) -> str:
    """Create playlist URL with a title from video ids and title."""
    return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"


def create_playlist_url_without_title(video_ids: str) -> str:
    """Create playlist URL without a title from video ids."""
    return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"
