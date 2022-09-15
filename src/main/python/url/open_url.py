"""module url.open_url"""

import logging
import webbrowser


def in_webbrowser(url: str) -> None:
    """
    The in_webbrowser function opens a URL in a new Web browser tab.

    :param url:str: Used to Pass a string to the function.
    :return: None.
    """
    logging.debug("Opening %s in new Web browser tab...", url)
    webbrowser.open_new_tab(url)
