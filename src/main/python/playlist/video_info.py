"""module playlist.video_info"""

import logging

from time_and_date import convert_time

from pytube import Playlist, YouTube, exceptions


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


def get_playlist_length(playlist_url: str) -> str:
    """
    The get_playlist_length function takes a YouTube playlist URL as an argument
    and returns the total length of all videos in the playlist.
    The function first creates a Playlist object from the YouTubePlaylist class,
    which takes in only one argument: the URL of the desired playlist.
    The Playlist object has a method called video_urls, which returns a list
    of URLs for each video in the playlist. We then iterate through this list
    to create individual YouTube objects using our custom YouTube class (which we imported).
    Each individual Youtube object has its own length attribute
    that can be accessed by calling .length on each instance.

    :param playlist_url:str: Used to Pass in the url of the playlist.
    :return: The total length of the playlist in hours, minutes, and seconds.
    """
    playlist_object = Playlist(playlist_url)

    video_duration_list = []
    for video_url in playlist_object.video_urls:
        youtube_object = YouTube(video_url)
        video_duration_list.append(youtube_object.length)

    return convert_time.convert_hours_minutes_seconds(sum(video_duration_list))
