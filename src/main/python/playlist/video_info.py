"""module playlist.video_info"""

import logging

from pytube import YouTube, exceptions


def get_video_info(video_id: str) -> dict[str]:
    """
    The get_video_info function accepts a YouTube video ID as an argument
    and returns the following:
        - The title of the video
        - A list of tags associated with the video
        - The length (in seconds) of the YouTube video

    :param video_id: Used to Specify the video that we want to get information about.
    :return: A dictionary containing information about the video.
    """
    try:
        yt = YouTube(f"http://youtube.com/watch?v={video_id}")
    except exceptions.PytubeError:
        logging.warning(f"Video id {video_id} is unavailable.")
        return {}
    if yt != {}:
        return {
            "title": yt.title,
            "author": yt.author,
            "channel_id": yt.channel_id,
            "channel_url": yt.channel_url,
            "thumbnail_url": yt.thumbnail_url,
            "description": yt.description,
            "keywords": yt.keywords,
            "length": yt.length,
            "publish_date": yt.publish_date,
            "rating": yt.rating,
            "views": yt.views,
        }
