"""main module"""
import contextlib
import logging
import random
import sys

import darkdetect
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtCore import Qt, QTranslator, pyqtSlot
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QTextEdit,
)
from qt_material import QtStyleTools, apply_stylesheet

from dialogs import import_playlist, reset_playlist
from dialogs.dialogs import show_error_dialog, show_info_dialog, show_question_dialog
from dialogs.settings_dialog import SettingsDialog
from file.file import check_file_format, read_file, read_json_file, write_json_file
from settings.operations import (
    get_menu_config,
    get_settings,
    output_menu_config_as_dict,
    output_settings_as_dict,
    save_menu_to_conf_file,
    save_settings_to_conf_file,
)
from strings import check_string, replace_string
from url import generate_url, open_url, url

APP_VERSION = "0.1.0"
RELEASE_DATE = "Sept 30 2022"

with contextlib.suppress(ImportError):
    from ctypes import windll  # Only exists on Windows

    APP_ID = f"christianhofmann.youtube-playlist-generator.gui.{APP_VERSION}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


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

    def initialize_ui(self) -> None:
        """Set up the application's GUI."""
        self.create_translator()
        self.create_license_dialog()
        self.set_theme()
        self.create_recent_file_menu()
        self.load_settings()

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

    def create_translator(self) -> None:
        """Create Translator for UI."""
        self.translator = QTranslator()
        self.translator.load(
            app_context.get_resource(
                "forms/translations/youtube-playlist-generator_eng.qm"
            )
        )
        app.installTranslator(self.translator)

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

    def create_recent_file_menu(self) -> None:
        """Create Open recent file menu."""
        self.file_menu = self.menuFile
        self.recent_files_menu = self.file_menu.addMenu("&Open recent")
        self.recent_files_menu.triggered.connect(self.act_recent_file)

    def get_recent_files_items_menu(self) -> list:
        return [action.text() for action in self.recent_files_menu.actions()[::-1]]

    def delete_unnecessary_entries_recent_file_menu(self) -> None:
        """Delete empty entries and Clear recent files items."""
        recent_files = self.get_recent_files_items_menu()
        while "" in recent_files:
            recent_files.remove("")
        while "Clear recent files" in recent_files:
            recent_files.remove("Clear recent files")

    def load_recent_files(self) -> None:
        """Add items to recent files."""
        menu_config = get_menu_config()

        if menu_config["recent_files"]:
            file_names = menu_config["recent_files"]
            logging.debug(file_names)
            for file_name in file_names:
                self.add_recent_filename(file_name)
            self.recent_files_menu.addSeparator()
            self.action = QAction()
            self.action.setText("Clear recent files")
            self.recent_files_menu.addAction(self.action)
        else:
            logging.info("No recent files!")
            self.delete_unnecessary_entries_recent_file_menu()

    def load_settings(self) -> None:
        """Load settings from menu.config."""
        self.load_recent_files()

    def save_settings(self) -> None:
        """Save settings to menu.config."""
        self.delete_unnecessary_entries_recent_file_menu()
        recent_files = self.get_recent_files_items_menu()
        menu_dict = output_menu_config_as_dict(recent_files)
        save_menu_to_conf_file(menu_dict)

    @pyqtSlot(QAction)
    def act_recent_file(self, action):
        """Action for click on one recent file."""
        if action.text() == "Clear recent files":
            actions = self.recent_files_menu.actions()
            for action_to_remove in actions:
                self.recent_files_menu.removeAction(action_to_remove)
        else:
            self.process_filename(action)

    def add_recent_filename(self, filename):
        """Add filename to recent file menu."""
        action = QAction(filename, self)
        actions = self.recent_files_menu.actions()
        before_action = actions[0] if actions else None
        self.recent_files_menu.insertAction(before_action, action)

    def open_ytplaylist_file_from_menu(self, action):
        """Open *.ytplaylist file from recent files menu."""
        filename = action.text()
        ytplaylist_dict = read_json_file(filename)
        if check_file_format(filename, ".ytplaylist"):
            if ytplaylist_dict:
                logging.debug("Playlist to be imported:")
                logging.debug(ytplaylist_dict)
                if self.check_if_items_in_playlist():
                    logging.debug("There are already items in playlist!")
                    dlg = import_playlist.PlaylistImportDialog()
                    if dlg.exec():
                        MainWindow.import_from_dict(self, ytplaylist_dict)
                    else:
                        MainWindow.act_new(self)
                        MainWindow.import_from_dict(self, ytplaylist_dict)
                        self.lineEdit_url_id.setFocus()
                    self.recent_files_menu.addSeparator()
                    self.new_action = QAction()
                    self.new_action.setText("Clear recent files")
                    self.recent_files_menu.addAction(self.new_action)
                else:
                    MainWindow.import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()
                self.pushButton_new.setEnabled(True)
                self.pushButton_delete_item.setEnabled(True)
                self.pushButton_generate.setEnabled(True)
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionReset_Playlist.setEnabled(True)
                self.actionDelete_Item.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)
                self.actionRename_item.setEnabled(True)
                self.actionSave.setEnabled(True)
                self.actionRemove_duplicates.setEnabled(True)
                self.menuSort_items.setEnabled(True)
                self.actionAscending.setEnabled(True)
                self.actionDescending.setEnabled(True)
                self.actionClear_all_items.setEnabled(True)
            else:
                show_error_dialog(
                    self,
                    "File not found!",
                    f"File '{filename}' not found!\n\nMaybe it was deleted?",
                )

                self.recent_files_menu.removeAction(action)
        else:
            show_error_dialog(
                self,
                "Wrong file format!",
                f"File '{filename}' is not a valid 'ytplaylist' file!",
            )

            self.recent_files_menu.removeAction(action)

    def process_filename(self, action):
        """Import YouTube Playlist file (*.ytplaylist)"""
        self.open_ytplaylist_file_from_menu(action)

    def closeEvent(self, event):
        """Save settings before app closes."""
        super().closeEvent(event)
        self.save_settings()

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

    def act_new(self) -> None:
        """
        Creates a blank state to start a new playlist.
        If the playlist already contains items and should be deleted
        remove all items in playlist and disable all buttons
        and clear playlist title field.
        """
        if MainWindow.playlist_widget_has_x_or_more_items(self, 1):
            dlg = reset_playlist.PlaylistResetDialog()
            if dlg.exec():
                self.listWidget_playlist_items.clear()
                logging.debug("Playlist was reset successfully.")
                if MainWindow.is_playlist_widget_empty(self):
                    MainWindow.disable_components(self)
                    self.pushButton_copy.setEnabled(False)
                    self.actionCopy_URL.setEnabled(False)
                    self.lineEdit_playlist_title.clear()
                    self.textEdit_playlist_generated_url.clear()
                    self.lineEdit_playlist_title.setFocus()
            else:
                logging.debug("Playlist reset cancelled.")
                logging.debug("No item was deleted!")
        else:
            self.listWidget_playlist_items.clear()
            logging.debug("Playlist was reset successfully.")
            if MainWindow.is_playlist_widget_empty(self):
                MainWindow.disable_components(self)
                self.pushButton_copy.setEnabled(False)
                self.actionCopy_URL.setEnabled(False)
                self.lineEdit_playlist_title.clear()
                self.textEdit_playlist_generated_url.clear()
                self.lineEdit_playlist_title.setFocus()

    def act_undo(self) -> None:
        """Undo last change."""
        print("Undo...")

    def act_redo(self) -> None:
        """Redo last change."""
        print("Redo...")

    def act_cut(self) -> None:
        """Cut text from selected text field."""
        print("Cut...")

    def act_copy(self) -> None:
        """Copy text from selected text field."""
        print("Copy...")

    def act_paste(self) -> None:
        """Paste text to selected text field."""
        print("Paste...")

    def act_select_all(self) -> None:
        """Select all tex from selected text field."""
        print("Select all...")

    def act_find(self) -> None:
        """Find text in playlist."""
        find_text, button_ok = QInputDialog.getText(self, "Find", "Playlist item:")

        if button_ok and find_text != "":
            try:
                item = self.listWidget_playlist_items.findItems(
                    find_text, Qt.MatchFlag.MatchRegularExpression
                )[0]
                item.setSelected(True)
                self.listWidget_playlist_items.scrollToItem(item)
            except IndexError:
                QMessageBox.warning(self, "Error!", f"No item '{find_text}' found!")

    def act_quit(self) -> None:
        """Quits the application."""
        app.quit()

    def act_count_items(self) -> None:
        """Opens CountItemsDialog and displays count of items in playlist."""
        QMessageBox.information(
            self,
            "Info",
            f"Number of items in playlist: {self.listWidget_playlist_items.count()}",
        )

    def act_clear_items(self) -> None:
        """
        Deletes all items in playlist.
        This is not the reset function!
        """
        self.listWidget_playlist_items.clear()
        logging.debug("All items in playlist deleted successfully.")
        show_info_dialog(
            self, "Success!", "All items in playlist deleted successfully."
        )
        if MainWindow.is_playlist_widget_empty(self):
            MainWindow.disable_components(self)
            self.pushButton_copy.setEnabled(False)
            self.actionCopy_URL.setEnabled(False)
            self.lineEdit_url_id.setFocus()

        if not MainWindow.playlist_widget_has_x_or_more_items(self, 1):
            self.actionClear_all_items.setEnabled(False)

    def act_sort_items_ascending(self) -> None:
        """Sort items in playlist ascending."""
        self.listWidget_playlist_items.setSortingEnabled(True)
        self.listWidget_playlist_items.sortItems(Qt.SortOrder.AscendingOrder)
        self.listWidget_playlist_items.setSortingEnabled(False)

    def act_sort_items_descending(self) -> None:
        """Sort items in playlist descending."""
        self.listWidget_playlist_items.setSortingEnabled(True)
        self.listWidget_playlist_items.sortItems(Qt.SortOrder.DescendingOrder)
        self.listWidget_playlist_items.setSortingEnabled(False)

    def act_url_id_text_change(self) -> None:
        """Enable Add button only if lineEdit_url_id is not empty."""
        if self.lineEdit_url_id.text() != "":
            self.pushButton_add.setEnabled(True)
            self.actionAdd_item.setEnabled(True)
        else:
            self.pushButton_add.setEnabled(False)
            self.actionAdd_item.setEnabled(False)

    def act_shuffle(self) -> None:
        """Shuffle playlist with random.shuffle()."""
        logging.debug("Shuffle playlist...")
        playlist = MainWindow.output_list_from_playlist_ids(self)
        random.shuffle(playlist)

        ytplaylist_dict = MainWindow.generate_dict_from_fields(
            self,
            self.lineEdit_playlist_title.text(),
            playlist,
        )

        self.listWidget_playlist_items.clear()
        MainWindow.import_from_dict(self, ytplaylist_dict)

    def act_about(self) -> QMessageBox:
        """Execute About QMessageBox."""
        return QMessageBox.about(
            self,
            "About YouTube Playlist Generator",
            f"""YouTube Playlist Generator by Christian Hofmann\n
            Version {APP_VERSION} ({RELEASE_DATE})""",
        )

    def act_about_qt(self) -> QMessageBox:
        """Execute About QMessageBox."""
        return QMessageBox.aboutQt(self)

    def act_license(self) -> QMessageBox:
        """Execute License Information as QMessageBox."""
        return self.license_dialog.exec()

    def act_contact(self) -> None:
        """Open default mail software with contact email address."""
        open_url.in_webbrowser("mailto:contact@youtube-playlist-generator.com")

    def act_report_a_bug(self) -> None:
        """Open Github issue page from project."""
        open_url.in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator/issues"
        )

    def act_github(self) -> None:
        """Open Github page from project."""
        open_url.in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator"
        )

    def act_rename_item(self) -> None:
        """Add flag ItemIsEditable to double clicked item in playlist."""
        list_widget = self.listWidget_playlist_items
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        MainWindow.make_item_editable(self)

    def make_item_editable(self) -> None:
        """Make item in playlist editable."""
        index = self.listWidget_playlist_items.currentIndex()
        if index.isValid():
            item = self.listWidget_playlist_items.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.listWidget_playlist_items.edit(index)

    def act_add_item(self) -> None:
        """
        Get content from textEdit field and convert URL to ID if necessary.
        Otherwise add new item to playlist.
        """
        text = self.lineEdit_url_id.text()
        if text != "":
            if check_string.is_string_valid_url(
                text
            ) and check_string.is_string_valid_youtube_url(text):
                user_id = url.cut_url_to_id(text)
                self.listWidget_playlist_items.addItem(str(user_id))

                item = self.listWidget_playlist_items.findItems(
                    user_id, Qt.MatchFlag.MatchRegularExpression
                )[0]
            else:
                self.listWidget_playlist_items.addItem(str(text))

                item = self.listWidget_playlist_items.findItems(
                    text, Qt.MatchFlag.MatchRegularExpression
                )[0]
            item.setSelected(True)
            self.listWidget_playlist_items.scrollToItem(item)

            self.lineEdit_url_id.clear()
            self.pushButton_new.setEnabled(True)
            self.pushButton_delete_item.setEnabled(True)
            self.actionDelete_Item.setEnabled(True)
            self.actionRename_item.setEnabled(True)
            self.actionReset_Playlist.setEnabled(True)

            if MainWindow.playlist_widget_has_x_or_more_items(self, 1):
                self.actionClear_all_items.setEnabled(True)

            if MainWindow.playlist_widget_has_x_or_more_items(self, 2):
                self.pushButton_generate.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionSave.setEnabled(True)
                self.actionRemove_duplicates.setEnabled(True)
                self.menuSort_items.setEnabled(True)
                self.actionAscending.setEnabled(True)
                self.actionDescending.setEnabled(True)

            if MainWindow.playlist_widget_has_x_or_more_items(self, 3):
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)

    def number_of_playlist_items(self) -> int:
        """Return number of items in playlist as int."""
        playlist = self.listWidget_playlist_items
        return len([playlist.item(x) for x in range(playlist.count())])

    def playlist_widget_has_x_or_more_items(self, number: int) -> bool:
        """Return True if one ore more items in playlist."""
        return MainWindow.number_of_playlist_items(self) >= number

    def is_playlist_widget_empty(self) -> bool:
        """Return True if no items in the playlist."""
        return MainWindow.number_of_playlist_items(self) == 0

    def disable_components(self) -> None:
        """Disable specific components."""
        self.pushButton_new.setEnabled(False)
        self.pushButton_delete_item.setEnabled(False)
        self.pushButton_generate.setEnabled(False)
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionReset_Playlist.setEnabled(False)
        self.actionDelete_Item.setEnabled(False)
        self.actionGenerate_Playlist.setEnabled(False)
        self.actionShuffle.setEnabled(False)
        self.actionRename_item.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionRemove_duplicates.setEnabled(False)
        self.textEdit_playlist_generated_url.setEnabled(False)

    def act_remove_duplicates(self) -> None:
        """Check if two or more items in playlist. Remove duplicates."""
        if MainWindow.playlist_widget_has_x_or_more_items(self, 2):
            MainWindow.remove_duplicates_from_playlist(self)

    def remove_duplicates_from_playlist(self) -> None:
        """If playlist contains duplicated items remove them from the list."""
        logging.debug("Remove duplicates from playlist:")
        show_info_dialog(self, "Success!", "Any duplicates have been deleted.")
        playlist = MainWindow.output_list_from_playlist_ids(self)
        logging.debug(playlist)

        playlist_without_duplicates = list(dict.fromkeys(playlist))

        ytplaylist_dict = MainWindow.generate_dict_from_fields(
            self,
            self.lineEdit_playlist_title.text(),
            playlist_without_duplicates,
        )

        self.listWidget_playlist_items.clear()
        MainWindow.import_from_dict(self, ytplaylist_dict)

        if not MainWindow.playlist_widget_has_x_or_more_items(self, 1):
            self.actionClear_all_items.setEnabled(False)

        if not MainWindow.playlist_widget_has_x_or_more_items(self, 2):
            self.actionRemove_duplicates.setEnabled(False)
            self.menuSort_items.setEnabled(False)
            self.actionAscending.setEnabled(False)
            self.actionDescending.setEnabled(False)

        if not MainWindow.playlist_widget_has_x_or_more_items(self, 3):
            self.pushButton_shuffle_playlist.setEnabled(False)

    def act_delete_item(self) -> [None, bool]:
        """If item selected delete it from the playlist."""
        list_items = self.listWidget_playlist_items.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listWidget_playlist_items.takeItem(
                self.listWidget_playlist_items.row(item)
            )
        if MainWindow.is_playlist_widget_empty(self):
            MainWindow.disable_components(self)

        elif not MainWindow.playlist_widget_has_x_or_more_items(self, 1):
            self.actionClear_all_items.setEnabled(False)

        elif not MainWindow.playlist_widget_has_x_or_more_items(self, 2):
            self.pushButton_generate.setEnabled(False)
            self.actionGenerate_Playlist.setEnabled(False)
            self.pushButton_shuffle_playlist.setEnabled(False)
            self.actionSave.setEnabled(False)
            self.actionRemove_duplicates.setEnabled(False)
            self.menuSort_items.setEnabled(False)
            self.actionAscending.setEnabled(False)
            self.actionDescending.setEnabled(False)
            self.actionClear_all_items.setEnabled(False)

        elif not MainWindow.playlist_widget_has_x_or_more_items(self, 3):
            self.pushButton_shuffle_playlist.setEnabled(False)
            self.actionShuffle.setEnabled(False)

    def act_copy_url(self) -> None:
        """Get content from textEdit_playlist_generated_url and copy it to clipboard."""
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def import_from_dict(self, ytplaylist_dict: dict) -> None:
        """Get content from dict and load it into the fields in the application."""
        playlist_title = ytplaylist_dict["playlistTitle"]
        playlist_ids = ytplaylist_dict["playlistIDs"]

        self.lineEdit_playlist_title.setText(playlist_title)
        logging.debug(playlist_ids)
        self.listWidget_playlist_items.addItems(playlist_ids)

    def check_if_items_in_playlist(self) -> bool:
        """Returns True if more than one item in playlist."""
        number_of_items = self.listWidget_playlist_items.count()
        logging.debug("Playlist items count: %s", number_of_items)
        return number_of_items >= 1

    def act_open(self) -> None:
        """Get path of .ytplaylist-file and import it via import_from_dict()."""
        try:
            if filename := QFileDialog.getOpenFileName(
                self,
                "Import YouTube Playlist file",
                "",
                "YouTube Playlist file (*.ytplaylist)",
            ):
                ytplaylist_dict = read_json_file(filename[0])
                logging.debug("Playlist to be imported:")
                logging.debug(ytplaylist_dict)
                if self.check_if_items_in_playlist():
                    logging.debug("There are already items in playlist!")
                    dlg = import_playlist.PlaylistImportDialog()

                    if dlg.exec():
                        MainWindow.import_from_dict(self, ytplaylist_dict)
                    else:
                        MainWindow.act_new(self)
                        MainWindow.import_from_dict(self, ytplaylist_dict)
                        self.lineEdit_url_id.setFocus()
                else:
                    MainWindow.import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()

                self.pushButton_new.setEnabled(True)
                self.pushButton_delete_item.setEnabled(True)
                self.pushButton_generate.setEnabled(True)
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionReset_Playlist.setEnabled(True)
                self.actionDelete_Item.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)
                self.actionRename_item.setEnabled(True)
                self.actionSave.setEnabled(True)
                self.actionRemove_duplicates.setEnabled(True)
                self.menuSort_items.setEnabled(True)
                self.actionAscending.setEnabled(True)
                self.actionDescending.setEnabled(True)
                self.actionClear_all_items.setEnabled(True)
                self.add_recent_filename(filename[0])
        except FileNotFoundError:
            logging.error("File not found. No file was imported.")

    def export_ytplaylist_file(self, filename: str, ytplaylist_dict: dict) -> None:
        """Write playlist title and playlist items from dict to given filename.ytplaylist file."""
        write_json_file(filename=filename, content=ytplaylist_dict)

    def generate_dict_from_fields(
        self, playlist_title: str, playlist_ids: list
    ) -> dict:
        """Return playlist items and title as dict."""
        return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}

    def output_list_from_playlist_ids(self) -> list:
        """Return playlist items as a list."""
        playlist = self.listWidget_playlist_items
        return [playlist.item(x).text() for x in range(playlist.count())]

    def act_save(self) -> None:
        """Get path to save .ytplaylist-file and generate file."""
        try:
            if filename := QFileDialog.getSaveFileName(
                self,
                "Export YouTube Playlist file",
                "",
                "YouTube Playlist file (*.ytplaylist)",
            ):
                logging.debug("Playlist exported under:")
                logging.debug(filename[0])
                ytplaylist_dict = MainWindow.generate_dict_from_fields(
                    self,
                    self.lineEdit_playlist_title.text(),
                    MainWindow.output_list_from_playlist_ids(self),
                )
                MainWindow.export_ytplaylist_file(self, filename[0], ytplaylist_dict)
        except FileNotFoundError:
            logging.error("Error during export process! No file was exported.")

    def act_generate(self) -> None:
        """
        Check if playlist title empty, ask if it should be added.
        Otherwise generate playlist URL.
        """

        if self.lineEdit_playlist_title.text() == "":
            if (
                show_question_dialog(
                    self,
                    "Your playlist title is currently empty",
                    "There is no title for playlist yet. Do you want to proceed?",
                )
                == QMessageBox.StandardButton.Yes
            ):
                MainWindow.generate_playlist(self)
        else:
            MainWindow.generate_playlist(self)

    def generate_playlist(self) -> None:
        """Generate playlist URL and enable copy button."""
        if not MainWindow.is_playlist_widget_empty(self):
            playlist = self.listWidget_playlist_items
            playlist_items = [playlist.item(x).text() for x in range(playlist.count())]

            comma_separated_string = MainWindow.create_comma_separated_string(
                self, playlist_items
            )
            MainWindow.generate_video_ids_url(self, comma_separated_string)

    def create_comma_separated_string(self, content_list: list) -> str:
        """Add commas after each item from list and return it as a string."""
        return ",".join(content_list)

    def generate_video_ids_url(self, comma_separated_string: str) -> None:
        """Generate the video ids URL from a comma separated string."""
        if self.lineEdit_playlist_title.text() == "":
            video_ids_url = url.create_playlist_url_without_title(
                self, comma_separated_string
            )

        elif check_string.has_space_in_string(self.lineEdit_playlist_title.text()):
            title_no_spaces = strings.replace_string.replace_space_in_string(
                self.lineEdit_playlist_title.text()
            )
            video_ids_url = url.create_playlist_url_with_title(
                comma_separated_string, title_no_spaces
            )
        else:
            video_ids_url = url.create_playlist_url_with_title(
                comma_separated_string, self.lineEdit_playlist_title.text()
            )
        playlist_url = generate_url.playlist_url(self, video_ids_url)
        if playlist_url != "":
            self.textEdit_playlist_generated_url.setText(playlist_url)
            self.textEdit_playlist_generated_url.setEnabled(True)
            self.pushButton_copy.setEnabled(True)
            self.actionCopy_URL.setEnabled(True)
            open_url.in_webbrowser(playlist_url)

    def show_error_creating_url_dialog(self) -> QMessageBox:
        """Show error creating URL dialog using show_error_dialog."""
        return show_error_dialog(
            self,
            "Error with creating playlist URL",
            "There was an error with creating the playlist URL."
            + "\n Check if all video ids are valid and correct.",
        )

    def act_settings(self) -> None:
        """Open settings dialog."""
        settings_dict = get_settings()
        dlg = SettingsDialog(self)
        SettingsDialog(self).load_settings(settings_dict)

        if dlg.exec():
            radio_button_os_state = dlg.radioButton_OS.isChecked()
            radio_button_white_state = dlg.radioButton_white.isChecked()
            radio_button_dark_state = dlg.radioButton_dark.isChecked()

            if radio_button_os_state:
                radio_button_theme = "os"
            elif radio_button_white_state:
                radio_button_theme = "white"
            elif radio_button_dark_state:
                radio_button_theme = "dark"

            components_dict = {
                "option_1": dlg.checkBox_option1.isChecked(),
                "option_2": dlg.checkBox_option2.isChecked(),
                "language": dlg.comboBox_language.currentText(),
                "theme": radio_button_theme,
                "shortcut_1": dlg.label_keyboard_shortcuts_option1.text(),
                "shortcut_2": dlg.label_keyboard_shortcuts_option2.text(),
                "shortcut_3": dlg.label_keyboard_shortcuts_option3.text(),
                "shortcut_4": dlg.label_keyboard_shortcuts_option4.text(),
                "shortcut_5": dlg.label_keyboard_shortcuts_option5.text(),
            }

            logging.debug(components_dict)
            settings_dict = output_settings_as_dict(components_dict)
            save_settings_to_conf_file(settings_dict)


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
