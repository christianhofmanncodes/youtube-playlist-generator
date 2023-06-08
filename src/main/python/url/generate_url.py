"""module url.generate_url"""

import logging

import requests

from dialogs import builtin_dialogs, creating_url


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
    if "\n" in video_ids_url:
        builtin_dialogs.show_error_dialog(
            self,
            "Not allowed character in URL",
            "Please check your video ids for not allowed characters!",
        )
        video_ids_url.replace("\n", "")
    try:
        response = requests.get(video_ids_url, verify=True, timeout=1000)
        logging.debug(response.status_code)
        playlist_link = response.url
        playlist_link = playlist_link.split("list=")[1]

        return f"https://www.youtube.com/playlist?list={playlist_link}&disable_polymer=true"

    except (requests.ConnectionError, IndexError, UnicodeEncodeError):
        creating_url.show_error_creating_url_dialog(self)
        logging.warning("An error occurred while generating the playlist URL!")
        return ""
