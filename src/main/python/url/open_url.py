"""module url.open_url"""

import logging
import webbrowser


def in_webbrowser(url: str) -> None:
    """Open a URL in Webbrowser in a new tab."""
    logging.debug("Opening %s in new Web browser tab...", url)
    webbrowser.open_new_tab(url)
