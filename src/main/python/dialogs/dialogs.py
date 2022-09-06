"""dialogs.dialogs module"""

from PyQt6.QtWidgets import QMessageBox


def show_question_dialog(self, title: str, text: str) -> QMessageBox:
    """Shows a predefined question dialog."""
    return QMessageBox.question(self, title, text)


def show_info_dialog(self, title: str, text: str) -> QMessageBox:
    """Shows a predefined info dialog."""
    return QMessageBox.information(self, title, text)


def show_error_dialog(self, title: str, text: str) -> QMessageBox:
    """Shows a predefined error dialog."""
    return QMessageBox.critical(self, title, text)


def show_warning_dialog(self, title: str, text: str) -> QMessageBox:
    """Shows a predefined warning dialog."""
    return QMessageBox.warning(self, title, text)
