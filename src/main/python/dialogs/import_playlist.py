"""dialogs.playlist_import_dialog module"""

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

app_context = ApplicationContext()


class PlaylistImportDialog(QDialog):
    """
    Class for the dialog to ask if you want to create a new playlist
    or if you want to add the imported playlist to the existing playlist.
    """

    def __init__(self, parent=None) -> None:
        """Build the dialog with its components."""
        super().__init__(parent)

        self.setWindowTitle("One more thing...")
        self.setFixedSize(450, 160)
        self.setWindowIcon(QIcon(app_context.get_resource("icon/youtube-play.icns")))
        self.setFont(QFont("Roboto"))

        q_btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message1 = QLabel("There are already items in the playlist!")
        message2 = QLabel(
            "Do you want to add the imported playlist to the existing playlist?"
        )
        message3 = QLabel(
            '"No" will delete your current playlist and create a new one.'
        )
        self.layout.addWidget(message1)
        self.layout.addWidget(message2)
        self.layout.addWidget(message3)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
