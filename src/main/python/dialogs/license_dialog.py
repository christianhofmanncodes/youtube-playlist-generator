"""module dialogs.license_dialog"""

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTextEdit

from file.file import read_file
from settings.settings import APP_ICON


def create_license_dialog(self, app_context) -> None:
    """
    The create_license_dialog function creates a license dialog.

    :param self: Used to Access the attributes and methods of the class.
    :return: The license_dialog object.
    """
    self.license_dialog = QDialog(self)
    self.license_text_object = QTextEdit(self.license_dialog)
    self.license_dialog.setMinimumSize(602, 400)
    self.license_dialog.setMaximumSize(602, 400)
    self.license_dialog.resize(602, 400)
    self.license_dialog.setWindowTitle("License information")
    self.license_dialog.setWindowIcon(QIcon(app_context.get_resource(APP_ICON)))

    self.license_text_object.setReadOnly(True)
    self.license_text_object.resize(602, 400)

    license_text = read_file(app_context.get_resource("forms/LICENSE.html"))

    self.license_text_object.setHtml(license_text)
