"""module playlist.video_info"""

import logging

from pytube import Playlist, Search, YouTube, exceptions

from time_and_date import convert_time


def get_video_info(video_id: str) -> dict:
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
        youtube_object = YouTube(f"https://youtube.com/watch?v={video_id}")
    except exceptions.PytubeError:
        logging.warning("Video id %s is unavailable.", video_id)
        youtube_object = {}

    return (
        {
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
        if youtube_object
        else {}
    )


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


def get_playlist_items(playlist_url: str) -> list:
    """
    The get_playlist_items function takes a YouTube playlist URL as input
    and returns a list of all the video URLs in that playlist.

    :param playlist_url:str: Used to specify the playlist URL.
    :return: A list of video URLs.
    """
    playlist_object = Playlist(playlist_url)
    return list(playlist_object.video_urls)


def search_for_videos(search_term: str) -> tuple:
    """
    The search_for_videos function takes a search term as an argument
    and returns a list of videos that match the search term.

    :param search_term:str: Used to Define the search term that will be used to find videos.
    :return: A list of results.
    """
    search_object = Search(search_term)
    logging.info(f"Found {len(search_object.results)} search results.")
    return search_object, search_object.results


def return_video_ids_from_search_object(search_object) -> list:
    """
    The return_video_ids_from_search_object function takes in a search object
    and returns a list of video ids.

    :param search_object: Used to Store the search results from a youtube api call.
    :return: A list of video ids.
    """
    return [search_result.video_id for search_result in search_object]


def get_more_search_results(search_object):
    """
    The get_more_search_results function takes a search object as input
    and returns the next set of results from that search.

    :param search_object: Used to Get the next page of results.
    :return: A new search object.
    """
    return search_object.get_next_results()
