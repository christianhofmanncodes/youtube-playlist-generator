"""module dialogs.creating_url"""

from PyQt6.QtWidgets import QMessageBox
from dialogs import dialogs


def show_error_creating_url_dialog(self) -> QMessageBox:
    """Show error creating URL dialog using show_error_dialog."""
    return dialogs.show_error_dialog(
        self,
        "Error with creating playlist URL",
        "There was an error with creating the playlist URL."
        + "\n Check if all video ids are valid and correct.",
    )
