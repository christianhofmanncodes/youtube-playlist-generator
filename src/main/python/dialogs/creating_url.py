"""module dialogs.creating_url"""

from dialogs import builtin_dialogs


def show_error_creating_url_dialog(self):
    """
    The show_error_creating_url_dialog function shows an error dialog
    when there is an error creating the playlist URL.
    It uses the show_error_dialog function to create and display the dialog.

    :param self: Used to Access the variables and methods inside of a class.
    :return: A QMessageBox object.
    """
    return builtin_dialogs.show_error_dialog(
        self,
        "Error with creating playlist URL",
        "There was an error with creating the playlist URL."
        + "\n Check if all video ids are valid and correct.",
    )
