"""module settings.settings"""

import contextlib


APP_VERSION = "0.1.0"
RELEASE_DATE = "Sept 30 2022"
RECENT_FILES_STRING = "Clear recent files"


with contextlib.suppress(ImportError):
    from ctypes import windll  # Only exists on Windows

    APP_ID = f"christianhofmann.youtube-playlist-generator.gui.{APP_VERSION}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
