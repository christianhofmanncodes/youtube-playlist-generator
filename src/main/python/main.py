"""main module"""
import logging
import sys

import darkdetect
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from qt_material import QtStyleTools, apply_stylesheet

from actions import actions
from dialogs import license
from menu import menu
from playlist import playlist
from settings import operations, settings
from settings.settings import RECENT_FILES_STRING


class MainWindow(QMainWindow, QtStyleTools):
    """
    Class for the main window with all its components and functions.
    """

    def __init__(self) -> None:
        """Connect MainWindow components with specific functions."""
        super().__init__()
        self.initialize_ui()
        self.create_actions()
        self.create_trigger()

        self.action = QAction()
        self.action.setText(RECENT_FILES_STRING)

    def initialize_ui(self) -> None:
        """Set up the application's GUI."""
        license.create_license_dialog(self)
        self.set_theme()
        operations.load_settings(self)

    def set_theme(self) -> None:
        """Check OS theme and apply to UI."""
        if darkdetect.isDark():
            invert_color = False
            app_theme = "theme/yt-dark-red.xml"
        elif darkdetect.isLight():
            invert_color = True
            app_theme = "theme/yt-white-red.xml"
        apply_stylesheet(
            app,
            theme=app_context.get_resource(app_theme),
            invert_secondary=invert_color,
        )
        uic.loadUi(app_context.get_resource("forms/main_window.ui"), self)
        self.setFont(QFont("Roboto"))

    def create_recent_file_menu(self) -> None:
        """Create Open recent file menu."""
        self.file_menu = self.menuFile
        self.recent_files_menu = self.file_menu.addMenu("&Open recent")
        self.recent_files_menu.triggered.connect(self.act_recent_file)

    def closeEvent(self, event):
        """Save settings before app closes."""
        super().closeEvent(event)
        operations.save_settings(self)

    def create_actions(self) -> None:
        """Create the applications menu actions."""
        self.actionNew.triggered.connect(self.act_new)
        self.actionOpen.triggered.connect(self.act_open)
        self.actionSave.triggered.connect(self.act_save)
        self.actionAbout.triggered.connect(self.act_about)
        self.actionSettings.triggered.connect(self.act_settings)
        self.actionQuit.triggered.connect(self.act_quit)

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
        self.actionCopy_URL.triggered.connect(self.act_copy_url)

        self.actionGithub.triggered.connect(self.act_github)
        self.actionReport_a_bug.triggered.connect(self.act_report_a_bug)
        self.actionContact.triggered.connect(self.act_contact)
        self.actionAbout_Qt.triggered.connect(self.act_about_qt)
        self.actionLicense.triggered.connect(self.act_license)

    def act_new(self):
        actions.act_new(self)

    def act_open(self):
        actions.act_open(self)

    def act_save(self):
        actions.act_save(self)

    def act_about(self):
        actions.act_about(self)

    def act_settings(self):
        actions.act_settings(self)

    def act_quit(self) -> None:
        """Quits the application."""
        app.quit()

    def act_undo(self):
        actions.act_undo(self)

    def act_redo(self):
        actions.act_redo(self)

    def act_cut(self):
        actions.act_cut(self)

    def act_copy(self):
        actions.act_copy(self)

    def act_paste(self):
        actions.act_paste(self)

    def act_select_all(self):
        actions.act_select_all(self)

    def act_find(self):
        actions.act_find(self)

    def act_add_item(self):
        actions.act_add_item(self)

    def act_delete_item(self):
        actions.act_delete_item(self)

    def act_rename_item(self):
        actions.act_rename_item(self)

    def act_shuffle(self):
        actions.act_shuffle(self)

    def act_generate(self):
        actions.act_generate(self)

    def act_sort_items_ascending(self):
        actions.act_sort_items_ascending(self)

    def act_sort_items_descending(self):
        actions.act_sort_items_descending(self)

    def act_count_items(self):
        actions.act_count_items(self)

    def act_clear_items(self):
        actions.act_clear_items(self)

    def act_remove_duplicates(self):
        actions.act_remove_duplicates(self)

    def act_copy_url(self):
        actions.act_copy_url(self)

    def act_github(self):
        actions.act_github(self)

    def act_report_a_bug(self):
        actions.act_report_a_bug(self)

    def act_contact(self):
        actions.act_contact(self)

    def act_about_qt(self):
        actions.act_about_qt(self)

    def act_license(self):
        actions.act_license(self)

    def act_recent_file(self):
        actions.act_recent_file(self, self.action)

    # TRIGGER:

    def act_url_id_text_change(self):
        actions.act_url_id_text_change(self)

    def act_add_item(self):
        actions.act_add_item(self)

    def act_rename_item(self):
        actions.act_rename_item(self)

    def create_trigger(self) -> None:
        """Create the trigger for several MainWindow components."""
        self.lineEdit_playlist_title.setFocus()
        self.lineEdit_url_id.textChanged.connect(self.act_url_id_text_change)
        self.pushButton_add.clicked.connect(self.act_add_item)
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.act_rename_item)
        self.pushButton_new.clicked.connect(self.act_new)
        self.pushButton_delete_item.clicked.connect(self.act_delete_item)
        self.pushButton_shuffle_playlist.clicked.connect(self.act_shuffle)
        self.pushButton_generate.clicked.connect(self.act_generate)
        self.pushButton_copy.clicked.connect(self.act_copy_url)


if __name__ == "__main__":
    app_context = ApplicationContext()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(
        QIcon(app_context.get_resource("icon/youtube-play.icns")),
    )

    window = MainWindow()
    window.show()

    exit_code = app_context.app.exec()
    sys.exit(exit_code)
