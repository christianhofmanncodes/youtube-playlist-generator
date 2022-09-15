"""module url.url"""


def cut_url_to_id(url: str) -> str:
    """
    The cut_url_to_id function takes a YouTube URL as an argument and returns the video ID.
    It does this by splitting the URL on either "v=" or "be/", returning the last item in
    the list, then removing any extra characters.

    :param url:str: Used to Pass the url of the video.
    :return: The id from the video url.
    """
    if "v=" in url:
        get_id = url.split("v=")
    elif "be/" in url:
        get_id = url.split("be/")
    return get_id[-1]


def create_playlist_url(video_ids: str, playlist_title: str, with_title: bool) -> str:
    """
    The create_playlist_url function creates a playlist URL from video ids and title, if title given.

    :param video_ids:str: Used to Pass the video ids of the videos to be added to a playlist.
    :param playlist_title:str: Used to Create a title for the playlist.
    :param with_title:bool: Used to Determine whether or not the playlist title should be included in the url.
    :return: The url of the playlist that is created from a list of video ids and a title.
    """

    """Create playlist URL with a title from video ids and title, if title given."""
    if with_title:
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"
    return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"
