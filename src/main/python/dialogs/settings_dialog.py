"""settings.settings module"""
import logging
import sys

import darkdetect
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QDialog
from qt_material import apply_stylesheet

app = QApplication(sys.argv)
app_context = ApplicationContext()


class SettingsDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, parent=None) -> None:
        """Load settings_dialog.ui file and connect components to their functions."""
        super().__init__(parent)
        uic.loadUi(
            app_context.get_resource("forms/settings_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource("icon/youtube-play.icns")))
        self.setFont(QFont("Roboto"))
        self.radioButton_OS.clicked.connect(self.change_theme)
        self.radioButton_white.clicked.connect(self.change_theme)
        self.radioButton_dark.clicked.connect(self.change_theme)
        self.pushButton_change_option1.clicked.connect(
            self.change_button_option1_clicked
        )
        self.pushButton_change_option2.clicked.connect(
            self.change_button_option2_clicked
        )
        self.pushButton_change_option3.clicked.connect(
            self.change_button_option3_clicked
        )
        self.pushButton_change_option4.clicked.connect(
            self.change_button_option4_clicked
        )
        self.pushButton_change_option5.clicked.connect(
            self.change_button_option5_clicked
        )

    def load_settings(self, settings_dict: dict) -> None:  # doesn't work yet
        """Display settings in dialog from dict."""
        open_url_automatically = settings_dict["general"][0]["openURLautomatically"]
        copy_url_to_clipboard = settings_dict["general"][0]["copyURLtoClipboard"]
        program_language = settings_dict["general"][0]["programLanguage"]
        app_theme = settings_dict["general"][0]["appTheme"]

        shortcut_import_new_playlist = settings_dict["keyboard_shortcuts"][0][
            "importNewPlaylist"
        ]
        shortcut_export_playlist = settings_dict["keyboard_shortcuts"][0][
            "exportPlaylist"
        ]
        shortcut_reset_playlist = settings_dict["keyboard_shortcuts"][0][
            "clearPlaylist"
        ]
        shortcut_generate_playlist = settings_dict["keyboard_shortcuts"][0][
            "generatePlaylist"
        ]
        shortcut_shuffle_playlist = settings_dict["keyboard_shortcuts"][0][
            "shufflePlaylist"
        ]

        self.comboBox_language.setCurrentText(program_language)

        if open_url_automatically is True:
            self.checkBox_option1.setCheckState(Qt.CheckState.Checked)

        elif open_url_automatically is False:
            self.checkBox_option1.setCheckState(Qt.CheckState.Unchecked)

        if copy_url_to_clipboard is True:
            self.checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_to_clipboard is False:
            self.checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        self.label_keyboard_shortcuts_option1.setText(shortcut_import_new_playlist)
        self.label_keyboard_shortcuts_option2.setText(shortcut_export_playlist)
        self.label_keyboard_shortcuts_option3.setText(shortcut_reset_playlist)
        self.label_keyboard_shortcuts_option4.setText(shortcut_generate_playlist)
        self.label_keyboard_shortcuts_option5.setText(shortcut_shuffle_playlist)

    def change_theme(self) -> None:
        """Change theme in runtime."""
        if self.radioButton_OS.isChecked():
            if darkdetect.isDark():
                apply_stylesheet(
                    app, theme=app_context.get_resource("theme/yt-dark-red.xml")
                )
                logging.debug("Theme regarding to OS theme set: %s", darkdetect.theme())
            elif darkdetect.isLight():
                apply_stylesheet(
                    app,
                    theme=app_context.get_resource("theme/yt-white-red.xml"),
                    invert_secondary=True,
                )
                logging.debug("Theme regarding to OS theme set: %s", darkdetect.theme())
        elif self.radioButton_white.isChecked():
            apply_stylesheet(
                app,
                theme=app_context.get_resource("theme/yt-white-red.xml"),
                invert_secondary=True,
            )
            logging.debug("White theme set!")
        elif self.radioButton_dark.isChecked():
            apply_stylesheet(
                app, theme=app_context.get_resource("theme/yt-dark-red.xml")
            )
            logging.debug("Dark theme set!")

    def change_language(self) -> None:
        """Change language in runtime."""
        pass

    def change_button_option1_clicked(self) -> None:
        """Get text from keySequenceEdit1 field and display in label."""
        if self.keySequenceEdit_option1.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option1.setText(
                self.keySequenceEdit_option1.keySequence().toString()
            )

    def change_button_option2_clicked(self) -> None:
        """Get text from keySequenceEdit2 field and display in label."""
        if self.keySequenceEdit_option2.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option2.setText(
                self.keySequenceEdit_option2.keySequence().toString()
            )

    def change_button_option3_clicked(self) -> None:
        """Get text from keySequenceEdit3 field and display in label."""
        if self.keySequenceEdit_option3.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option3.setText(
                self.keySequenceEdit_option3.keySequence().toString()
            )

    def change_button_option4_clicked(self) -> None:
        """Get text from keySequenceEdit4 field and display in label."""
        if self.keySequenceEdit_option4.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option4.setText(
                self.keySequenceEdit_option4.keySequence().toString()
            )

    def change_button_option5_clicked(self) -> None:
        """Get text from keySequenceEdit5 field and display in label."""
        if self.keySequenceEdit_option5.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option5.setText(
                self.keySequenceEdit_option5.keySequence().toString()
            )
