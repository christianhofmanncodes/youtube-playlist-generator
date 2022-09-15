"""module playlist.video_info"""

import lxml
import urllib
from lxml import etree


def get_title__channel_from_youtube_link(video_id) -> str:
    """
    The get_title__channel_from_youtube_link function takes a YouTube video ID as an argument and returns the title of the video.

    :param video_id: Used to Specify the video id of the youtube link.
    :return: The title of the video from the youtube link.
    """
    youtube = etree.HTML(
        urllib.request.urlopen(f"https://www.youtube.com/watch?v={video_id}").read()
    )

    video_title = youtube.xpath("//meta[@name='title']/@content")

    if video_title != [""]:
        video_information = f"{video_title}"
        return "".join(video_information)


def get_video_thumbnail_url_from_video_id(video_id) -> str:
    """
    The get_video_thumbnail_url_from_video_id function accepts a video id and returns the url of the video's thumbnail.

    :param video_id: Used to Specify the video id.
    :return: The url of the video thumbnail.
    """
    return etree.HTML(
        urllib.request.urlopen(
            f"img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        ).read()
    )
