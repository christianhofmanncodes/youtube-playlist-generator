"""dialogs.playlist_reset_dialog module"""

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

app_context = ApplicationContext()


class PlaylistResetDialog(QDialog):
    """
    Class for the dialog to ask if the playlist should be deleted with all its components.
    """

    def __init__(self, parent=None) -> None:
        """Build the dialog with its components."""
        super().__init__(parent)

        self.setWindowTitle("Are you sure?")
        self.setFixedSize(450, 140)
        self.setWindowIcon(QIcon(app_context.get_resource("config/settings.config")))
        self.setFont(QFont("Roboto"))

        q_btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(
            "Do you really want to reset your playlist? That deletes all of your items!"
        )
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
