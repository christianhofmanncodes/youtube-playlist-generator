"""dialogs.dialogs module"""

from PyQt6.QtWidgets import QMessageBox


def show_question_dialog(self, title: str, text: str):
    """
    The show_question_dialog function shows a predefined question dialog.

    :param self: Used to Access the attributes and methods of the class.
    :param title:str: Used to Set the title of the dialog window.
    :param text:str: Used to Set the text of the dialog.
    :return: A value of type QMessageBox.
    """
    return QMessageBox.question(self, title, text)


def show_info_dialog(self, title: str, text: str):
    """
    The show_info_dialog function shows a predefined info dialog.

    :param self: Used to Access the attributes and methods of the class.
    :param title:str: Used to Set the title of the dialog window.
    :param text:str: Used to Set the text of the dialog.
    :return: A value of type QMessageBox.
    """
    return QMessageBox.information(self, title, text)


def show_error_dialog(self, title: str, text: str):
    """
    The show_error_dialog function shows a predefined error dialog.

    :param self: Used to Access the attributes and methods of the class.
    :param title:str: Used to Set the title of the dialog window.
    :param text:str: Used to Set the text of the dialog.
    :return: A value of type QMessageBox.
    """
    return QMessageBox.critical(self, title, text)


def show_warning_dialog(self, title: str, text: str):
    """
    The show_warning_dialog function shows a predefined warning dialog.

    :param self: Used to Access the attributes and methods of the class.
    :param title:str: Used to Set the title of the dialog window.
    :param text:str: Used to Set the text of the dialog.
    :return: A value of type QMessageBox.
    """
    return QMessageBox.warning(self, title, text)
