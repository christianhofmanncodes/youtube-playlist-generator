"""module dialogs.restart_app"""

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from settings.settings import APP_ICON


class RestartAppDialog(QDialog):
    """
    Class for the dialog to ask if the program should be restarted.
    """

    def __init__(self, app_context, parent=None) -> None:
        """
        The __init__ function is called when an instance of the class is created.
        It initializes variables that are defined in the body of the class, and it sets up
        the initial state of its attributes. It can take arguments as input (e.g., parent).
        The __init__ function is used to initialize all member variables.

        :param self: Used to Access the variables and methods of the class.
        :param parent=None: Used to Pass the parent widget of this dialog.
        :return: None.
        """
        super().__init__(parent)

        self.setWindowTitle("Program needs to be restarted")
        self.setFixedSize(450, 140)
        self.setWindowIcon(QIcon(app_context.get_resource(APP_ICON)))
        self.setFont(QFont("Roboto"))

        q_btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.vbox_layout = QVBoxLayout()
        message = QLabel(
            """To update the language settings the program needs to be restarted.
            Do you want to restart now?"""
        )
        self.vbox_layout.addWidget(message)
        self.vbox_layout.addWidget(self.button_box)
        self.setLayout(self.vbox_layout)
