"""main module"""
import logging
import sys

import darkdetect
from fbs_runtime import platform
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtCore import QLocale, QTranslator
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from qt_material import QtStyleTools, apply_stylesheet

from actions import actions
from dialogs import license_dialog
from settings.operations import get_settings, load_settings, save_settings
from settings.settings import (
    APP_ICON,
    APP_VERSION,
    DARK_THEME_LOCATION,
    SETTING_FILE_LOCATION,
    WHITE_THEME_LOCATION,
)

if platform.is_windows():
    from ctypes import windll

    APP_ID = f"christianhofmann.youtube-playlist-generator.gui.{APP_VERSION}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

logging.info("OS: %s", platform.name())


class MainWindow(QMainWindow, QtStyleTools):
    """
    Class for the main window with all its components and functions.
    """

    def __init__(self) -> None:
        """
        The __init__ function is called automatically every time the class is
        instantiated. It sets up all of the attributes and performs any initializing
        code.

        :param self: Used to Reference the object itself.
        :return: None.
        """
        super().__init__()
        self.initialize_ui()
        self.create_actions()
        self.create_trigger()
        self.translate_ui()

    def initialize_ui(self) -> None:
        """
        The initialize_ui function sets up the application's GUI.
        It creates a license dialog box and sets the theme for the application.

        :param self: Used to Access the attributes and methods of the class MainWindow.
        :return: None.
        """
        license_dialog.create_license_dialog(self, app_context)
        self.set_theme()
        load_settings(self, app_context)

    def set_theme(self) -> None:
        """
        The set_theme function checks the OS theme and applies a stylesheet to the UI.
        If the OS is dark, it will apply a dark stylesheet. If it's light, it will apply
        a light one.

        :param self: Used to Access the attributes and methods of the class.
        :return: None.
        """
        invert_color = False
        app_theme = DARK_THEME_LOCATION

        if darkdetect.isDark():
            invert_color = False
            app_theme = DARK_THEME_LOCATION
        elif darkdetect.isLight():
            invert_color = True
            app_theme = WHITE_THEME_LOCATION

        settings_theme = self.compare_os_with_settings_theme()

        if settings_theme is not None:
            if settings_theme == "dark":
                app_theme = DARK_THEME_LOCATION
                invert_color = False
            elif settings_theme == "white":
                app_theme = WHITE_THEME_LOCATION
                invert_color = True

        apply_stylesheet(
            app,
            theme=app_context.get_resource(app_theme),
            invert_secondary=invert_color,
        )

        uic.loadUi(app_context.get_resource("forms/main_window.ui"), self)
        self.setFont(QFont("Roboto"))
        self.compare_os_with_settings_theme()

    def compare_os_with_settings_theme(self) -> str | None:
        """
        The compare_os_with_settings_theme function compares the OS theme to the settings theme.
        Return appTheme if they mismatch.

        :param self: Used to Reference the class instance.
        :return: The appTheme if the os theme and settings theme mismatch.
        """
        settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)

        if darkdetect.theme().lower() != settings_dict["general"][0]["appTheme"]:
            return settings_dict["general"][0]["appTheme"]
        return None

    def create_actions(self) -> None:
        """
        The create_actions function creates the applications menu actions.
        The function connects each action to its corresponding slot method.

        :param self: Used to Access the attributes and methods of the class.
        :return: None.
        """
        self.actionNew.triggered.connect(self.act_new)
        self.actionOpen.triggered.connect(self.act_open)
        self.actionSave.triggered.connect(self.act_save)
        self.actionAbout.triggered.connect(self.act_about)
        self.actionSettings.triggered.connect(self.act_settings)

        self.actionUndo.triggered.connect(self.act_undo)
        self.actionRedo.triggered.connect(self.act_redo)
        self.actionCut.triggered.connect(self.act_cut)
        self.actionCopy.triggered.connect(self.act_copy)
        self.actionPaste.triggered.connect(self.act_paste)
        self.actionSelect_all.triggered.connect(self.act_select_all)
        self.actionFind.triggered.connect(self.act_find)

        self.actionAdd_item.triggered.connect(self.act_add_item)
        self.actionDelete_Item.triggered.connect(self.act_delete_item)
        self.actionRename_item.triggered.connect(self.act_rename_item)
        self.actionShuffle.triggered.connect(self.act_shuffle)
        self.actionGenerate_Playlist.triggered.connect(self.act_generate)
        self.actionAscending.triggered.connect(self.act_sort_items_ascending)
        self.actionDescending.triggered.connect(self.act_sort_items_descending)
        self.actionCount_items.triggered.connect(self.act_count_items)
        self.actionClear_all_items.triggered.connect(self.act_clear_items)
        self.actionRemove_duplicates.triggered.connect(self.act_remove_duplicates)
        self.actionGet_video_information.triggered.connect(self.act_video_information)
        self.actionCopy_URL.triggered.connect(self.act_copy_url)

        self.actionGithub.triggered.connect(self.act_github)
        self.actionReport_a_bug.triggered.connect(self.act_report_a_bug)
        self.actionContact.triggered.connect(self.act_contact)
        self.actionAbout_Qt.triggered.connect(self.act_about_qt)
        self.actionLicense.triggered.connect(self.act_license)

    def act_new(self):
        """Action for new."""
        actions.act_new(self, app_context)

    def act_open(self):
        """Action for open."""
        actions.act_open(self, app_context)

    def act_save(self):
        """Action for save."""
        actions.act_save(self)

    def act_about(self):
        """Action for about."""
        actions.act_about(self)

    def act_settings(self):
        """Action for settings."""
        actions.act_settings(self, app, app_context)

    def closeEvent(self, event) -> None:
        """
        The closeEvent function is called when the user closes the application.
        It saves the settings and closes the application.

        :param self: Used to Access the attributes and methods of the class in which it is used.
        :param event: Used to Close the application.
        :return: The event that is generated when the user tries to close the application window.
        """
        save_settings(self, app_context)
        logging.info("All settings saved successfully.")
        app.quit()

    def act_undo(self):
        """Action for undo."""
        actions.act_undo(self)

    def act_redo(self):
        """Action for redo."""
        actions.act_redo(self)

    def act_cut(self):
        """Action for cut."""
        actions.act_cut(self)

    def act_copy(self):
        """Action for copy."""
        actions.act_copy(self)

    def act_paste(self):
        """Action for paste."""
        actions.act_paste(self)

    def act_select_all(self):
        """Action for select_all."""
        actions.act_select_all(self)

    def act_find(self):
        """Action for find."""
        actions.act_find(self)

    def act_add_item(self):
        """Action for add_item."""
        actions.act_add_item(self)

    def act_delete_item(self):
        """Action for delete_item."""
        actions.act_delete_item(self)

    def act_rename_item(self):
        """Action for rename_item."""
        actions.act_rename_item(self)

    def act_shuffle(self):
        """Action for shuffle."""
        actions.act_shuffle(self)

    def act_generate(self):
        """Action for generate."""
        actions.act_generate(self, app_context)

    def act_sort_items_ascending(self):
        """Action for sort_items_ascending."""
        actions.act_sort_items_ascending(self)

    def act_sort_items_descending(self):
        """Action for sort_items_descending."""
        actions.act_sort_items_descending(self)

    def act_count_items(self):
        """Action for count_items."""
        actions.act_count_items(self)

    def act_clear_items(self):
        """Action for clear_items."""
        actions.act_clear_items(self)

    def act_remove_duplicates(self):
        """Action for remove_duplicates."""
        actions.act_remove_duplicates(self)

    def act_video_information(self):
        """Action when item in playlist clicked."""
        actions.act_video_information(self)

    def act_copy_url(self):
        """Action for copy_url."""
        actions.act_copy_url(self)

    def act_github(self):
        """Action for github."""
        actions.act_github()

    def act_report_a_bug(self):
        """Action for report_a_bug."""
        actions.act_report_a_bug()

    def act_contact(self):
        """Action for contact."""
        actions.act_contact()

    def act_about_qt(self):
        """Action for about_qt."""
        actions.act_about_qt(self)

    def act_license(self):
        """Action for license."""
        actions.act_license(self)

    def act_recent_file(self, app_context, action):
        """Action for recent_file."""
        actions.act_recent_file(self, app_context, action)

    def act_url_id_text_change(self):
        """Action for url_id_text_change."""
        actions.act_url_id_text_change(self)

    def act_click_playlist_item(self):
        """Action for click_playlist_item."""
        actions.act_click_playlist_item(self)

    def create_trigger(self) -> None:
        """
        The create_trigger function creates the trigger for several MainWindow components.
        The lineEdit_playlist_title is set to focus, and the lineEdit_url_id text is changed.
        The button add button calls act_add item when clicked, and the listWidget playlist items
        double click calls act rename item when clicked. The pushButton new button calls act new
        when clicked, the pushButton delete item button clicks act delete item when clicked,
        and the shuffle playlists pushes call shuffle playlist when pushed.

        :param self: Used to Access the class attributes and methods.
        :return: None.
        """
        self.lineEdit_playlist_title.setFocus()
        self.lineEdit_url_id.textChanged.connect(self.act_url_id_text_change)
        self.listWidget_playlist_items.itemSelectionChanged.connect(
            self.act_click_playlist_item
        )
        self.pushButton_add.clicked.connect(self.act_add_item)
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.act_rename_item)
        self.pushButton_new.clicked.connect(self.act_new)
        self.pushButton_delete_item.clicked.connect(self.act_delete_item)
        self.pushButton_shuffle_playlist.clicked.connect(self.act_shuffle)
        self.pushButton_generate.clicked.connect(self.act_generate)
        self.pushButton_copy.clicked.connect(self.act_copy_url)

    def install_translator(self, settings_dict) -> None:
        """Installs the Translator based on the program language settings."""
        if settings_dict["general"][0]["programLanguage"] == "English":
            logging.info("Program language is English.")

        elif settings_dict["general"][0]["programLanguage"] == "Deutsch":
            data = app_context.get_resource("forms/translations/de/MainWindow.qm")
            german = QLocale(QLocale.Language.German, QLocale.Country.Germany)
            self.trans.load(german, data)
            app.instance().installTranslator(self.trans)

        elif settings_dict["general"][0]["programLanguage"] == "Español":
            data = app_context.get_resource("forms/translations/es-ES/MainWindow.qm")
            german = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
            self.trans.load(german, data)
            app.instance().installTranslator(self.trans)

    def translate_menu(self) -> None:
        """Translates the Menu based on language settings"""
        self.menuFile.setTitle(app.translate("MainWindow", "&File"))
        self.actionNew.setText(app.translate("MainWindow", "New playlist"))
        self.actionOpen.setText(app.translate("MainWindow", "Open"))
        self.actionSave.setText(app.translate("MainWindow", "Save"))
        self.actionAbout.setText(app.translate("MainWindow", "About"))
        self.actionSettings.setText(app.translate("MainWindow", "Settings"))
        self.actionQuit.setText(app.translate("MainWindow", "Quit"))

        self.menuEdit.setTitle(app.translate("MainWindow", "&Edit"))
        self.actionUndo.setText(app.translate("MainWindow", "Undo"))
        self.actionRedo.setText(app.translate("MainWindow", "Redo"))
        self.actionCut.setText(app.translate("MainWindow", "Cut"))
        self.actionCopy.setText(app.translate("MainWindow", "Copy"))
        self.actionPaste.setText(app.translate("MainWindow", "Paste"))
        self.actionSelect_all.setText(app.translate("MainWindow", "Select All"))
        self.actionFind.setText(app.translate("MainWindow", "Find"))

        self.menuPlaylist.setTitle(app.translate("MainWindow", "&Playlist"))
        self.actionAdd_item.setText(app.translate("MainWindow", "Add item"))
        self.actionDelete_Item.setText(app.translate("MainWindow", "Delete item"))
        self.actionRename_item.setText(app.translate("MainWindow", "Rename item"))
        self.actionShuffle.setText(app.translate("MainWindow", "Shuffle"))
        self.actionGenerate_Playlist.setText(app.translate("MainWindow", "Generate"))

        self.menuSort_items.setTitle(app.translate("MainWindow", "Sort items"))
        self.actionAscending.setText(app.translate("MainWindow", "Ascending"))
        self.actionDescending.setText(app.translate("MainWindow", "Descending"))

        self.menuTools.setTitle(app.translate("MainWindow", "Tools"))
        self.actionCount_items.setText(app.translate("MainWindow", "Count items"))
        self.actionClear_all_items.setText(
            app.translate("MainWindow", "Clear all items")
        )
        self.actionGet_video_information.setText(
            app.translate("MainWindow", "Get video information")
        )
        self.actionRemove_duplicates.setText(
            app.translate("MainWindow", "Remove duplicates")
        )

        self.actionCopy_URL.setText(app.translate("MainWindow", "Copy URL"))

        self.menuHelp.setTitle(app.translate("MainWindow", "&Help"))
        self.actionAbout_Qt.setText(app.translate("MainWindow", "About Qt"))
        self.actionContact.setText(app.translate("MainWindow", "Contact"))
        self.actionGithub.setText(app.translate("MainWindow", "GitHub"))
        self.actionLicense.setText(app.translate("MainWindow", "License"))
        self.actionReport_a_bug.setText(app.translate("MainWindow", "Report a bug"))

    def translate_main_window(self) -> None:
        """Translates the MainWindow based on language settings"""
        self.lineEdit_playlist_title.setPlaceholderText(
            app.translate("MainWindow", "Playlist title")
        )
        self.lineEdit_url_id.setPlaceholderText(
            app.translate("MainWindow", "URL or ID")
        )

        self.pushButton_new.setText(app.translate("MainWindow", "New"))
        self.pushButton_delete_item.setText(app.translate("MainWindow", "Delete Item"))
        self.pushButton_shuffle_playlist.setText(app.translate("MainWindow", "Shuffle"))
        self.pushButton_generate.setText(app.translate("MainWindow", "Generate"))

        self.textEdit_playlist_generated_url.setPlaceholderText(
            app.translate("MainWindow", "Playlist URL will show up here...")
        )

    def translate_tooltips(self) -> None:
        """Translates the tooltips based on language settings"""
        self.lineEdit_playlist_title.setToolTip(
            app.translate("MainWindow", "Add a playlist title here")
        )
        self.lineEdit_url_id.setToolTip(app.translate("MainWindow", "Enter URL or ID"))
        self.pushButton_add.setToolTip(app.translate("MainWindow", "Add new item"))
        self.pushButton_new.setToolTip(
            app.translate("MainWindow", "Create new playlist")
        )
        self.pushButton_delete_item.setToolTip(
            app.translate("MainWindow", "Delete selected item")
        )
        self.pushButton_shuffle_playlist.setToolTip(
            app.translate("MainWindow", "Apply Shuffle")
        )
        self.pushButton_generate.setToolTip(
            app.translate("MainWindow", "Generate Playlist URL")
        )
        self.textEdit_playlist_generated_url.setToolTip(
            app.translate("MainWindow", "Playlist URL")
        )
        self.pushButton_copy.setToolTip(
            app.translate("MainWindow", "Copy generated URL")
        )

    def translate_ui(self) -> None:
        """Translates the UI based on language settings"""
        self.trans = QTranslator(self)

        settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)

        self.install_translator(settings_dict)
        self.translate_menu()
        self.translate_main_window()
        self.translate_tooltips()


if __name__ == "__main__":
    app_context = ApplicationContext()

    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(
        QIcon(app_context.get_resource(APP_ICON)),
    )

    window = MainWindow()
    window.show()

    exit_code = app_context.app.exec()
    sys.exit(exit_code)
