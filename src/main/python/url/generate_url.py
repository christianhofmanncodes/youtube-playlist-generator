"""module url.generate_url"""

import logging
import ssl
from urllib import error, request

from dialogs import creating_url


def playlist_url(self, video_ids_url: str) -> str:
    """
    The playlist_url function generates the playlist URL from the video ids URL.
    It is called by the create_playlist function and takes one argument, which is
    the video ids URL.

    :param self: Used to Access the variables and methods of the class.
    :param video_ids_url:str: Used to Get the video ids from the user input.
    :return: The url of the playlist that is generated from the video ids url.
    """
    if not video_ids_url.lower().startswith("https"):
        raise ValueError from None
    try:
        ctx = ssl._create_default_https_context()
        with request.urlopen(video_ids_url, context=ctx) as response:
            playlist_link = response.geturl()
            playlist_link = playlist_link.split("list=")[1]

        return f"https://www.youtube.com/playlist?list={playlist_link}&disable_polymer=true"

    except (error.URLError, IndexError, UnicodeEncodeError):
        creating_url.show_error_creating_url_dialog(self)
        logging.warning("An error occurred while generating the playlist URL!")
        return ""
