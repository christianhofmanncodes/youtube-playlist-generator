"""module dialogs.settings_dialog"""

import logging
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QDialog
import darkdetect
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from qt_material import apply_stylesheet

from dialogs import restart_app
from settings.operations import (
    check_if_settings_not_default,
    get_default_settings,
    get_settings,
    save_settings_to_conf_file,
)
from settings.settings import (
    APP_ICON,
    DEFAULT_SETTINGS_FILE_LOCATION,
    SETTING_FILE_LOCATION,
)
from translate import translator


app = QApplication(sys.argv)
app_context = ApplicationContext()


class SettingsDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, app, app_context, parent=None) -> None:
        """
        The __init__ function is called automatically every time
        the class is being used to create a new object.
        The first argument of every class method, including init,
        is always a reference to the current instance of the class.
        By convention, this argument is always named self.
        In init __self__ refers to the newly created object; in other
        class methods, it refers to the instance whose method was called.

        :param self: Used to Access the attributes and methods of the class.
        :param parent=None: Used to Ensure that the dialog box does not close when it is launched.
        :return: None.
        """

        super().__init__(parent)
        uic.loadUi(
            app_context.get_resource("forms/settings_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource(APP_ICON)))
        self.setFont(QFont("Roboto"))

        self.translate_ui()
        self.translate_settings()
        self.enable_reset_default_settings(app_context)

        self.radioButton_OS.clicked.connect(self.change_to_os_theme)
        self.radioButton_white.clicked.connect(self.change_to_white_theme)
        self.radioButton_dark.clicked.connect(self.change_to_dark_theme)
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
        self.pushButton_change_option6.clicked.connect(
            self.change_button_option6_clicked
        )
        self.pushButton_change_option7.clicked.connect(
            self.change_button_option7_clicked
        )
        self.pushButton_change_option8.clicked.connect(
            self.change_button_option8_clicked
        )
        self.pushButton_change_option9.clicked.connect(
            self.change_button_option9_clicked
        )
        self.pushButton_change_option10.clicked.connect(
            self.change_button_option10_clicked
        )
        self.pushButton_change_option11.clicked.connect(
            self.change_button_option11_clicked
        )
        self.pushButton_change_option12.clicked.connect(
            self.change_button_option12_clicked
        )
        self.pushButton_change_option13.clicked.connect(
            self.change_button_option13_clicked
        )
        self.pushButton_reset_defaults.clicked.connect(
            self.reset_button_defaults_clicked
        )

    def load_settings(self, settings_dict: dict) -> None:
        """
        The load_settings function loads the settings from a dictionary into the dialog.
        The function takes one argument, which is a dictionary containing all of the settings.

        :param self: Used to Access variables, methods etc in the rest of the class.
        :param settings_dict:dict: Used to Pass the settings_dict to the function.
        :return: None.
        """
        open_url = settings_dict["general"][0]["openURL"]
        copy_url_to_clipboard = settings_dict["general"][0]["copyURLtoClipboard"]
        program_language = settings_dict["general"][0]["programLanguage"]
        app_theme = settings_dict["general"][0]["appTheme"]

        shortcut_new_playlist = settings_dict["keyboard_shortcuts"][0]["newPlaylist"]
        shortcut_open_playlist = settings_dict["keyboard_shortcuts"][0]["openPlaylist"]
        shortcut_save_playlist = settings_dict["keyboard_shortcuts"][0]["savePlaylist"]
        shortcut_add_item = settings_dict["keyboard_shortcuts"][0]["addItem"]
        shortcut_delete_item = settings_dict["keyboard_shortcuts"][0]["deleteItem"]
        shortcut_rename_item = settings_dict["keyboard_shortcuts"][0]["renameItem"]
        shortcut_shuffle_playlist = settings_dict["keyboard_shortcuts"][0][
            "shufflePlaylist"
        ]

        shortcut_generate_playlist = settings_dict["keyboard_shortcuts"][0][
            "generatePlaylist"
        ]
        shortcut_count_items = settings_dict["keyboard_shortcuts"][0]["countItems"]
        shortcut_clear_all_items = settings_dict["keyboard_shortcuts"][0][
            "clearAllItems"
        ]
        shortcut_get_video_information = settings_dict["keyboard_shortcuts"][0][
            "getVideoInformation"
        ]
        shortcut_remove_duplicates = settings_dict["keyboard_shortcuts"][0][
            "removeDuplicates"
        ]
        shortcut_copy_url = settings_dict["keyboard_shortcuts"][0]["copyURL"]

        self.comboBox_language.setCurrentText(program_language)

        if open_url is True:
            self.checkBox_option1.setCheckState(Qt.CheckState.Checked)

        elif open_url is False:
            self.checkBox_option1.setCheckState(Qt.CheckState.Unchecked)

        if copy_url_to_clipboard is True:
            self.checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_to_clipboard is False:
            self.checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        self.label_keyboard_shortcuts_option1.setText(shortcut_new_playlist)
        self.label_keyboard_shortcuts_option2.setText(shortcut_open_playlist)
        self.label_keyboard_shortcuts_option3.setText(shortcut_save_playlist)
        self.label_keyboard_shortcuts_option4.setText(shortcut_add_item)
        self.label_keyboard_shortcuts_option5.setText(shortcut_delete_item)
        self.label_keyboard_shortcuts_option6.setText(shortcut_rename_item)
        self.label_keyboard_shortcuts_option7.setText(shortcut_shuffle_playlist)
        self.label_keyboard_shortcuts_option8.setText(shortcut_generate_playlist)
        self.label_keyboard_shortcuts_option9.setText(shortcut_count_items)
        self.label_keyboard_shortcuts_option10.setText(shortcut_clear_all_items)
        self.label_keyboard_shortcuts_option11.setText(shortcut_get_video_information)
        self.label_keyboard_shortcuts_option12.setText(shortcut_remove_duplicates)
        self.label_keyboard_shortcuts_option13.setText(shortcut_copy_url)

        if app_theme == "os":
            self.radioButton_OS.nextCheckState()
        elif app_theme == "white":
            self.radioButton_white.nextCheckState()
        elif app_theme == "dark":
            self.radioButton_dark.nextCheckState()

    def translate_ui(self):
        """Translates the UI based on language settings"""
        settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)
        translator.install_translator(
            self, app, app_context, settings_dict, "SettingsDialog.qm"
        )

    def translate_settings(self) -> None:
        """Translates the SettingsDialog based on language settings"""
        self.setWindowTitle(
            app.translate("SettingsDialog", "Settings"),
        )
        self.tabWidget.setTabText(0, app.translate("SettingsDialog", "General"))
        self.groupBox_General.setTitle(app.translate("SettingsDialog", "General"))
        self.checkBox_option1.setText(
            app.translate(
                "SettingsDialog", "Open URL in Web Browser after playlist was generated"
            ),
        )
        self.checkBox_option2.setText(
            app.translate(
                "SettingsDialog", "Copy URL to clipboard after playlist was generated"
            )
        )
        self.groupBox_language.setTitle(app.translate("SettingsDialog", "Language"))
        self.groupBox_theme.setTitle(app.translate("SettingsDialog", "Theme"))
        self.pushButton_reset_defaults.setText(
            app.translate("SettingsDialog", "Reset to defaults")
        )

        self.tabWidget.setTabText(
            1, app.translate("SettingsDialog", "Keyboard Shortcuts")
        )

        self.groupBox_keyboard_shortcuts.setTitle(
            app.translate("SettingsDialog", "Keyboard Shortcuts")
        )
        self.label_keyboard_shortcuts_option1_text.setText(
            app.translate("SettingsDialog", "New playlist")
        )
        self.label_keyboard_shortcuts_option2_text.setText(
            app.translate("SettingsDialog", "Open playlist")
        )
        self.label_keyboard_shortcuts_option3_text.setText(
            app.translate("SettingsDialog", "Save playlist")
        )
        self.label_keyboard_shortcuts_option4_text.setText(
            app.translate("SettingsDialog", "Add item")
        )
        self.label_keyboard_shortcuts_option5_text.setText(
            app.translate("SettingsDialog", "Delete item")
        )
        self.label_keyboard_shortcuts_option6_text.setText(
            app.translate("SettingsDialog", "Rename item")
        )
        self.label_keyboard_shortcuts_option7_text.setText(
            app.translate("SettingsDialog", "Shuffle")
        )
        self.label_keyboard_shortcuts_option8_text.setText(
            app.translate("SettingsDialog", "Generate")
        )
        self.label_keyboard_shortcuts_option9_text.setText(
            app.translate("SettingsDialog", "Count items")
        )
        self.label_keyboard_shortcuts_option10_text.setText(
            app.translate("SettingsDialog", "Clear all items")
        )
        self.label_keyboard_shortcuts_option11_text.setText(
            app.translate("SettingsDialog", "Get video information")
        )
        self.label_keyboard_shortcuts_option12_text.setText(
            app.translate("SettingsDialog", "Remove duplicates")
        )
        self.label_keyboard_shortcuts_option13_text.setText(
            app.translate("SettingsDialog", "Copy URL")
        )

        self.pushButton_change_option1.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option2.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option3.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option4.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option5.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option6.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option7.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option8.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option9.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option10.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option11.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option12.setText(
            app.translate("SettingsDialog", "Change")
        )
        self.pushButton_change_option13.setText(
            app.translate("SettingsDialog", "Change")
        )

    def change_to_os_theme(self) -> None:
        """
        The change_to_os_theme function changes the theme to the OS theme.
        It detects if the OS theme is dark and sets the theme to dark.
        If the OS theme is light, it sets the theme to white.
        It is called when a user clicks on the radio button radioButton_os.

        :param self: Used to Access the attributes and methods of the class in python.
        :return: None.
        """
        if darkdetect.isDark():
            apply_stylesheet(
                app, theme=app_context.get_resource("theme/yt-dark-red.xml")
            )
        elif darkdetect.isLight():
            apply_stylesheet(
                app,
                theme=app_context.get_resource("theme/yt-white-red.xml"),
                invert_secondary=True,
            )
            logging.debug("Theme regarding to OS theme set: %s", darkdetect.theme())

    def change_to_dark_theme(self) -> None:
        """
        The change_to_dark_theme function changes the theme to dark.
        It is called when a user clicks on the radio button radioButton_dark.

        :param self: Used to Access the attributes and methods of the class in python.
        :return: None.
        """
        apply_stylesheet(app, theme=app_context.get_resource("theme/yt-dark-red.xml"))
        logging.debug("Dark theme set!")

    def change_to_white_theme(self) -> None:
        """
        The change_to_white_theme function changes the theme to white.
        It is called when a user clicks on the radio button radioButton_white.

        :param self: Used to Access the attributes and methods of the class in python.
        :return: None.
        """
        apply_stylesheet(
            app,
            theme=app_context.get_resource("theme/yt-white-red.xml"),
            invert_secondary=True,
        )
        logging.debug("White theme set!")

    def change_button_option1_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option1.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option2_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option2.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option3_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option3.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option4_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option4.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option5_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option5.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option6_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option6.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option7_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option7.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option8_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option8.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option9_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option9.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option10_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option10.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option11_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option11.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option12_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option12.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option13_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option13.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def reset_button_defaults_clicked(self) -> None:
        """
        The reset_button_defaults_clicked function resets all settings to default values.
        It does this by reading the default settings from a file, and then saving those
        defaults to a configuration file. The function then loads the defaults into the GUI.

        :param self: Used to Access the class attributes and methods.
        :return: None.
        """
        default_settings_dict = get_default_settings(
            DEFAULT_SETTINGS_FILE_LOCATION, app_context
        )
        save_settings_to_conf_file(
            default_settings_dict, SETTING_FILE_LOCATION, app_context
        )
        settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)
        self.load_settings(settings_dict)

    def enable_reset_default_settings(self, app_context) -> None:
        """
        The enable_reset_default_settings function enables
        the reset to default settings button if the current
        settings are not equal to the default settings.

        :param self: Used to Access the class attributes.
        :return: None.
        """
        if check_if_settings_not_default(self, app_context):
            self.pushButton_reset_defaults.setEnabled(True)

    def restart_if_confirmed(self, app, app_context) -> None:
        """Show dialog to restart application."""
        dlg = restart_app.RestartAppDialog(app_context)
        if dlg.exec():
            app.exit(-123456789)
