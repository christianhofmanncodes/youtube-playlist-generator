"""module dialogs.license"""

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file.file import read_file
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTextEdit

app_context = ApplicationContext()


def create_license_dialog(self) -> None:
    """Create license dialog."""
    self.license_dialog = QDialog(self)
    self.license_text_object = QTextEdit(self.license_dialog)
    self.license_dialog.setMinimumSize(602, 400)
    self.license_dialog.setMaximumSize(602, 400)
    self.license_dialog.resize(602, 400)
    self.license_dialog.setWindowTitle("License information")
    self.license_dialog.setWindowIcon(
        QIcon(app_context.get_resource("icon/youtube-play.icns"))
    )

    self.license_text_object.setReadOnly(True)
    self.license_text_object.resize(602, 400)

    license_text = read_file(app_context.get_resource("forms/LICENSE.html"))

    self.license_text_object.setHtml(license_text)
