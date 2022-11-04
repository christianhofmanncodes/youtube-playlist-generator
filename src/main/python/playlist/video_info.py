"""module playlist.video_info"""

import logging

from pytube import YouTube, exceptions


def get_video_info(video_id: str) -> dict | None:
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
        youtube_object = YouTube(f"http://youtube.com/watch?v={video_id}")
    except exceptions.PytubeError:
        logging.warning("Video id %s is unavailable.", video_id)
        youtube_object = {}

    if youtube_object != {}:
        return {
            "title": youtube_object.title,
            "author": youtube_object.author,
            "channel_id": youtube_object.channel_id,
            "channel_url": youtube_object.channel_url,
            "thumbnail_url": youtube_object.thumbnail_url,
            "description": youtube_object.description,
            "keywords": youtube_object.keywords,
            "length": youtube_object.length,
            "publish_date": youtube_object.publish_date,
            "rating": youtube_object.rating,
            "views": youtube_object.views,
        }
    return None
