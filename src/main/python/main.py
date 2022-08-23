"""main module"""
import contextlib
import json
import logging
import random
import ssl
import sys
import webbrowser
from urllib import error, request

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)
from qt_material import apply_stylesheet, QtStyleTools

with contextlib.suppress(ImportError):
    from ctypes import windll  # Only exists on Windows

    APP_ID = "christianhofmann.youtube-playlist-generator.gui.0.1.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Ui(QMainWindow):
    """
    Class for the main window with all its components and functions.
    """

    def __init__(self):
        """Connect UI components with specific functions."""
        super(Ui, self).__init__()
        self.initializeUI()
        self.createActions()
        self.createTrigger()

    def initializeUI(self):
        """Set up the application's GUI."""
        uic.loadUi(app_context.get_resource("forms/form.ui"), self)
        self.setFont(QFont("Roboto"))

    def createActions(self):
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

    def createTrigger(self):
        """Create the trigger for several UI components."""
        self.lineEdit_playlist_title.setFocus()
        self.lineEdit_url_id.textChanged.connect(self.act_url_id_text_change)
        self.pushButton_add.clicked.connect(self.act_add_item)
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.act_rename_item)
        self.pushButton_new.clicked.connect(self.act_new)
        self.pushButton_delete_item.clicked.connect(self.act_delete_item)
        self.pushButton_shuffle_playlist.clicked.connect(self.act_shuffle)
        self.pushButton_generate.clicked.connect(self.act_generate)
        self.pushButton_copy.clicked.connect(self.act_copy_url)
        self.listWidget_playlist_items.itemSelectionChanged.connect(
            self.display_number_of_item_in_statusbar
        )

    def display_number_of_item_in_statusbar(self):
        """Display the number of selected item in playlist in statusbar."""
        self.statusBar.showMessage(
            f"Selected playlist item: {str(self.listWidget_playlist_items.currentRow() + 1)}"
        )

    def act_drag_drop(self):
        print("Wow!")

    def act_new(self):
        """
        Creates a blank state to start a new playlist.
        If the playlist already contains items and should be deleted
        remove all items in playlist and disable all buttons
        and clear playlist title field.
        """
        if Ui.playlist_widget_has_one_or_more_items(self):
            dlg = AskPlaylistResetDialog(self)
            if dlg.exec():
                self.listWidget_playlist_items.clear()
                logging.debug("Playlist was reset successfully.")
                if Ui.is_playlist_widget_empty(self):
                    Ui.disable_components(self)
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
            if Ui.is_playlist_widget_empty(self):
                Ui.disable_components(self)
                self.pushButton_copy.setEnabled(False)
                self.actionCopy_URL.setEnabled(False)
                self.lineEdit_playlist_title.clear()
                self.textEdit_playlist_generated_url.clear()
                self.lineEdit_playlist_title.setFocus()

    def act_undo(self):
        """Undo last change."""
        pass

    def act_redo(self):
        """Redo last change."""
        pass

    def act_cut(self):
        """Cut text from selected text field."""
        pass

    def act_copy(self):
        """Copy text from selected text field."""
        pass

    def act_paste(self):
        """Paste text to selected text field."""
        pass

    def act_select_all(self):
        """Select all tex from selected text field."""
        pass

    def act_find(self):
        find_text, ok = QInputDialog.getText(self, "Find", "Playlist item:")

        if ok and find_text != "":
            try:
                item = self.listWidget_playlist_items.findItems(
                    find_text, Qt.MatchFlag.MatchRegularExpression
                )[0]
                item.setSelected(True)
                self.listWidget_playlist_items.scrollToItem(item)
            except IndexError:
                QMessageBox.warning(self, "Error!", f"No item '{find_text}' found!")

    def act_quit(self):
        """Quits the application."""
        app.quit()

    def act_count_items(self):
        """Opens CountItemsDialog and displays count of items in playlist."""
        QMessageBox.information(
            self,
            "Info",
            f"Number of items in playlist: {self.listWidget_playlist_items.count()}",
        )

    def act_clear_items(self):
        """
        Deletes all items in playlist.
        This is not the reset function!
        """
        self.listWidget_playlist_items.clear()
        logging.debug("All items in playlist deleted successfully.")
        Ui.show_info_dialog(
            self, "Success!", "All items in playlist deleted successfully."
        )
        if Ui.is_playlist_widget_empty(self):
            Ui.disable_components(self)
            self.pushButton_copy.setEnabled(False)
            self.actionCopy_URL.setEnabled(False)
            self.lineEdit_url_id.setFocus()

        if not Ui.playlist_widget_has_one_or_more_items(self):
            self.actionClear_all_items.setEnabled(False)

    def act_sort_items_ascending(self):
        """Sort items in playlist ascending."""
        self.listWidget_playlist_items.setSortingEnabled(True)
        self.listWidget_playlist_items.sortItems(Qt.SortOrder.AscendingOrder)
        self.listWidget_playlist_items.setSortingEnabled(False)

    def act_sort_items_descending(self):
        """Sort items in playlist descending."""
        self.listWidget_playlist_items.setSortingEnabled(True)
        self.listWidget_playlist_items.sortItems(Qt.SortOrder.DescendingOrder)
        self.listWidget_playlist_items.setSortingEnabled(False)

    def act_url_id_text_change(self):
        """Enable Add button only if lineEdit_url_id is not empty."""
        if self.lineEdit_url_id.text() != "":
            self.pushButton_add.setEnabled(True)
            self.actionAdd_item.setEnabled(True)
        else:
            self.pushButton_add.setEnabled(False)
            self.actionAdd_item.setEnabled(False)

    def act_shuffle(self):
        """Shuffle playlist with random.shuffle()."""
        logging.debug("Shuffle playlist...")
        playlist = Ui.output_list_from_playlist_ids(self)
        random.shuffle(playlist)

        ytplaylist_dict = Ui.generate_dict_from_fields(
            self,
            self.lineEdit_playlist_title.text(),
            playlist,
        )

        self.listWidget_playlist_items.clear()
        Ui.import_from_dict(self, ytplaylist_dict)

    def act_about(self):
        """Execute InfoDialog."""
        dlg = InfoDialog(self)
        dlg.exec()

    def act_contact(self):
        """Open default mail software with contact email address."""
        self.open_url_in_webbrowser("mailto:contact@youtube-playlist-generator.com")

    def act_report_a_bug(self):
        """Open Github issue page from project."""
        self.open_url_in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator/issues"
        )

    def act_github(self):
        """Open Github page from project."""
        self.open_url_in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator"
        )

    def act_rename_item(self, item):
        """Add flag ItemIsEditable to double clicked item in playlist."""
        list_widget = self.listWidget_playlist_items
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        Ui.make_item_editable(self)

    def make_item_editable(self):
        """Make item in playlist editable."""
        index = self.listWidget_playlist_items.currentIndex()
        if index.isValid():
            item = self.listWidget_playlist_items.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.listWidget_playlist_items.edit(index)

    def act_add_item(self):
        """
        Get content from textEdit field and convert URL to ID if necessary.
        Otherwise add new item to playlist.
        """
        text = self.lineEdit_url_id.text()
        if text != "":
            if Ui.is_string_valid_url(self, text) and Ui.is_string_valid_youtube_url(
                self, text
            ):
                user_id = Ui.cut_url_to_id(self, text)
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

            if Ui.playlist_widget_has_one_or_more_items(self):
                self.actionClear_all_items.setEnabled(True)

            if Ui.playlist_widget_has_two_or_more_items(self):
                self.pushButton_generate.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionSave.setEnabled(True)
                self.actionRemove_duplicates.setEnabled(True)
                self.menuSort_items.setEnabled(True)
                self.actionAscending.setEnabled(True)
                self.actionDescending.setEnabled(True)

            if Ui.playlist_widget_has_three_or_more_items(self):
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)

    def is_string_valid_url(self, string):
        """Check if http:// or https:// in string and return bool value."""
        return "http://" in string or "https://" in string

    def is_string_valid_youtube_url(self, string):
        """Check if watch? or be/ in string and return bool value."""
        return "watch?" in string or "be/" in string

    def cut_url_to_id(self, url):
        """Return id from video URL."""
        if "v=" in url:
            get_id = url.split("v=")
        elif "be/" in url:
            get_id = url.split("be/")
        return get_id[-1]

    def number_of_playlist_items(self):
        """Return number of items in playlist as int."""
        playlist = self.listWidget_playlist_items
        return len([playlist.item(x) for x in range(playlist.count())])

    def playlist_widget_has_one_or_more_items(self):
        """Return True if one ore more items in playlist."""
        return Ui.number_of_playlist_items(self) >= 1

    def playlist_widget_has_two_or_more_items(self):
        """Return True if two ore more items in playlist."""
        return Ui.number_of_playlist_items(self) >= 2

    def playlist_widget_has_three_or_more_items(self):
        """Return True if three or more items in playlist."""
        return Ui.number_of_playlist_items(self) >= 3

    def is_playlist_widget_empty(self):
        """Return True if no items in the playlist."""
        return Ui.number_of_playlist_items(self) == 0

    def disable_components(self):
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

    def act_remove_duplicates(self):
        """Check if two or more items in playlist. Remove duplicates."""
        if Ui.playlist_widget_has_two_or_more_items(self):
            Ui.remove_duplicates_from_playlist(self)

    def remove_duplicates_from_playlist(self):
        """If playlist contains duplicated items remove them from the list."""
        logging.debug("Remove duplicates from playlist:")
        Ui.show_info_dialog(self, "Success!", "Any duplicates have been deleted.")
        playlist = Ui.output_list_from_playlist_ids(self)
        logging.debug(playlist)

        playlist_without_duplicates = list(dict.fromkeys(playlist))

        ytplaylist_dict = Ui.generate_dict_from_fields(
            self,
            self.lineEdit_playlist_title.text(),
            playlist_without_duplicates,
        )

        self.listWidget_playlist_items.clear()
        Ui.import_from_dict(self, ytplaylist_dict)

        if not Ui.playlist_widget_has_one_or_more_items(self):
            self.actionClear_all_items.setEnabled(False)

        if not Ui.playlist_widget_has_two_or_more_items(self):
            self.actionRemove_duplicates.setEnabled(False)
            self.menuSort_items.setEnabled(False)
            self.actionAscending.setEnabled(False)
            self.actionDescending.setEnabled(False)

        if not Ui.playlist_widget_has_three_or_more_items(self):
            self.pushButton_shuffle_playlist.setEnabled(False)

    def act_delete_item(self):
        """If item selected delete it from the playlist."""
        list_items = self.listWidget_playlist_items.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listWidget_playlist_items.takeItem(
                self.listWidget_playlist_items.row(item)
            )
        if Ui.is_playlist_widget_empty(self):
            Ui.disable_components(self)

        elif not Ui.playlist_widget_has_one_or_more_items(self):
            self.actionClear_all_items.setEnabled(False)

        elif not Ui.playlist_widget_has_two_or_more_items(self):
            self.pushButton_generate.setEnabled(False)
            self.actionGenerate_Playlist.setEnabled(False)
            self.pushButton_shuffle_playlist.setEnabled(False)
            self.actionSave.setEnabled(False)
            self.actionRemove_duplicates.setEnabled(False)
            self.menuSort_items.setEnabled(False)
            self.actionAscending.setEnabled(False)
            self.actionDescending.setEnabled(False)
            self.actionClear_all_items.setEnabled(False)

        elif not Ui.playlist_widget_has_three_or_more_items(self):
            self.pushButton_shuffle_playlist.setEnabled(False)
            self.actionShuffle.setEnabled(False)

    def has_text_edit_playlist_generated_url_content(self):  # deprecated
        """Return True if textEdit_playlist_generated_url is not empty."""
        return self.textEdit_playlist_generated_url.toPlainText() != ""

    def act_copy_url(self):
        """Get content from textEdit_playlist_generated_url and copy it to clipboard."""
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def read_json_file(self, filename):
        """Return content from json-file."""
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
        return data

    def import_from_dict(self, ytplaylist_dict):
        """Get content from dict and load it into the fields in the application."""
        playlist_title = ytplaylist_dict["playlistTitle"]
        playlist_ids = ytplaylist_dict["playlistIDs"]

        self.lineEdit_playlist_title.setText(playlist_title)
        logging.debug(playlist_ids)
        self.listWidget_playlist_items.addItems(playlist_ids)

    def check_if_items_in_playlist(self):
        """Returns True if more than one item in playlist."""
        number_of_items = self.listWidget_playlist_items.count()
        logging.debug(f"Playlist items count: {number_of_items}")
        return number_of_items >= 1

    def return_number_of_items_in_playlist(self):  # deprecated
        """Returns number of items in playlist."""
        number_of_items = self.listWidget_playlist_items.count()
        logging.debug(f"Playlist items count: {number_of_items}")
        return number_of_items

    def act_open(self):
        """Get path of .ytplaylist-file and import it via import_from_dict()."""
        try:
            if filename := QFileDialog.getOpenFileName(
                self,
                "Import YouTube Playlist file",
                "",
                "YouTube Playlist file (*.ytplaylist)",
            ):
                ytplaylist_dict = Ui.read_json_file(self, filename[0])
                logging.debug("Playlist to be imported:")
                logging.debug(ytplaylist_dict)
                if self.check_if_items_in_playlist():
                    logging.debug("There are already items in playlist!")
                    dlg = AskPlaylistImport(self)

                    if dlg.exec():
                        Ui.import_from_dict(self, ytplaylist_dict)
                    else:
                        Ui.act_new(self)
                        Ui.import_from_dict(self, ytplaylist_dict)
                        self.lineEdit_url_id.setFocus()
                else:
                    Ui.import_from_dict(self, ytplaylist_dict)
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
        except FileNotFoundError:
            logging.error("File not found. No file was imported.")

    def export_ytplaylist_file(self, filename, ytplaylist_dict):
        """Write playlist title and playlist items from dict to given filename.ytplaylist file."""
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(ytplaylist_dict, file, indent=4)

    def generate_dict_from_fields(self, playlist_title, playlist_ids):
        """Return playlist items and title as dict."""
        return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}

    def output_list_from_playlist_ids(self):
        """Return playlist items as a list."""
        playlist = self.listWidget_playlist_items
        return [playlist.item(x).text() for x in range(playlist.count())]

    def act_save(self):
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
                ytplaylist_dict = Ui.generate_dict_from_fields(
                    self,
                    self.lineEdit_playlist_title.text(),
                    Ui.output_list_from_playlist_ids(self),
                )
                Ui.export_ytplaylist_file(self, filename[0], ytplaylist_dict)
        except FileNotFoundError:
            logging.error("Error during export process! No file was exported.")

    def show_question_dialog(self, title, text):
        """Shows a predefined question dialog."""
        return QMessageBox.question(self, title, text)

    def show_info_dialog(self, title, text):
        """Shows a predefined info dialog."""
        return QMessageBox.information(self, title, text)

    def show_error_dialog(self, title, text):
        """Shows a predefined error dialog."""
        return QMessageBox.critical(self, title, text)

    def show_warning_dialog(self, title, text):
        """Shows a predefined warning dialog."""
        return QMessageBox.warning(self, title, text)

    def act_generate(self):
        """
        Check if playlist title empty, ask if it should be added.
        Otherwise generate playlist URL.
        """

        if self.lineEdit_playlist_title.text() == "":
            if (
                Ui.show_question_dialog(
                    self,
                    "Your playlist title is currently empty",
                    "There is no title for playlist yet. Do you want to proceed?",
                )
                == QMessageBox.StandardButton.Yes
            ):
                Ui.generate_playlist(self)
        else:
            Ui.generate_playlist(self)

    def generate_playlist(self):
        """Generate playlist URL and enable copy button."""
        if not Ui.is_playlist_widget_empty(self):
            playlist = self.listWidget_playlist_items
            playlist_items = [playlist.item(x).text() for x in range(playlist.count())]

            comma_separated_string = Ui.create_comma_separated_string(
                self, playlist_items
            )
            Ui.generate_video_ids_url(self, comma_separated_string)

    def create_comma_separated_string(self, content_list):
        """Add commas after each item from list and return it as a string."""
        return ",".join(content_list)

    def generate_video_ids_url(self, comma_separated_string):
        """Generate the video ids URL from a comma separated string."""
        if self.lineEdit_playlist_title.text() == "":
            video_ids_url = Ui.create_playlist_url_without_title(
                self, comma_separated_string
            )

        elif Ui.has_space_in_title(self, self.lineEdit_playlist_title.text()):
            title_no_spaces = Ui.replace_space_in_title(
                self, self.lineEdit_playlist_title.text()
            )
            video_ids_url = Ui.create_playlist_url_with_title(
                self, comma_separated_string, title_no_spaces
            )
        else:
            video_ids_url = Ui.create_playlist_url_with_title(
                self, comma_separated_string, self.lineEdit_playlist_title.text()
            )
        playlist_url = self.generate_playlist_url(video_ids_url)
        if playlist_url != "":
            self.textEdit_playlist_generated_url.setText(playlist_url)
            self.textEdit_playlist_generated_url.setEnabled(True)
            self.pushButton_copy.setEnabled(True)
            self.actionCopy_URL.setEnabled(True)
            Ui.open_playlist_url_in_webbrowser(self, playlist_url)

    def has_space_in_title(self, title):
        """Return True if space in title."""
        return " " in title

    def replace_space_in_title(self, title_with_space):
        """Add URL encoding to playlist title."""
        return title_with_space.replace(" ", "%20")

    def create_playlist_url_with_title(self, video_ids, playlist_title):
        """Create playlist URL with a title from video ids and title."""
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"

    def create_playlist_url_without_title(self, video_ids):
        """Create playlist URL without a title from video ids."""
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"

    def show_error_creating_url_dialog(self):
        """Show error creating URL dialog using show_error_dialog."""
        return Ui.show_error_dialog(
            self,
            "Error with creating playlist URL",
            "There was an error with creating the playlist URL."
            + "\n Check if all video ids are valid and correct.",
        )

    def generate_playlist_url(self, video_ids_url):
        """Generate the playlist URL from the video ids URL."""
        try:
            context = ssl._create_unverified_context()
            with request.urlopen(video_ids_url, context=context) as response:
                playlist_link = response.geturl()
                playlist_link = playlist_link.split("list=")[1]

            return (
                f"https://www.youtube.com/playlist?list={playlist_link}"
                + "&disable_polymer=true"
            )
        except (error.URLError, IndexError, UnicodeEncodeError):
            Ui.show_error_creating_url_dialog(self)
            logging.warning("An error occurred while generating the playlist URL!")
            return ""

    def open_url_in_webbrowser(self, url):
        """Open a URL in Webbrowser in a new tab."""
        logging.debug(f"\nOpening {url} in new Web browser tab...\n")
        webbrowser.open_new_tab(url)

    def open_playlist_url_in_webbrowser(self, playlist_url):
        """Open the generated playlist URL in Webbrowser."""
        Ui.open_url_in_webbrowser(self, playlist_url)

    def save_settings_to_conf_file(self, settings_dict):
        """Write content from dict to settings.config."""
        with open(
            app_context.get_resource("config/settings.config"),
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(settings_dict, file, indent=4)

    def load_settings(self, settings_dict):
        """Display settings in dialog from dict."""
        program_language = settings_dict["programLanguage"]
        open_url_automatically = settings_dict["openURLautomatically"]
        copy_url_to_clipboard = settings_dict["copyURLtoClipboard"]

        shortcut_import_new_playlist = settings_dict["keyboardShortcuts"][0][
            "importNewPlaylist"
        ]
        shortcut_export_playlist = settings_dict["keyboardShortcuts"][0][
            "exportPlaylist"
        ]
        shortcut_reset_playlist = settings_dict["keyboardShortcuts"][0]["clearPlaylist"]
        shortcut_generate_playlist = settings_dict["keyboardShortcuts"][0][
            "generatePlaylist"
        ]

        SettingsDialog(self).comboBox_language.setCurrentText(program_language)

        if open_url_automatically is True:
            SettingsDialog(self).checkBox_option1.setCheckState(Qt.CheckState.Checked)

        elif open_url_automatically is False:
            SettingsDialog(self).checkBox_option1.setCheckState(Qt.CheckState.Unchecked)

        if copy_url_to_clipboard is True:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_to_clipboard is False:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        key_sequence_import_new_playlist = QKeySequence.fromString(
            shortcut_import_new_playlist,
            format=QKeySequence.SequenceFormat.PortableText,
        )

        SettingsDialog(self).label_keyboard_shortcuts_option1.setText(
            shortcut_import_new_playlist
        )

        SettingsDialog(self).keySequenceEdit_option1.setKeySequence(
            key_sequence_import_new_playlist
        )

        SettingsDialog(self).keySequenceEdit_option2.setKeySequence(
            shortcut_export_playlist
        )

        SettingsDialog(self).keySequenceEdit_option3.setKeySequence(
            shortcut_reset_playlist
        )

        SettingsDialog(self).keySequenceEdit_option4.setKeySequence(
            shortcut_generate_playlist
        )

    def get_settings(self):
        """Return content from settings.config."""
        return Ui.read_json_file(
            self,
            app_context.get_resource("config/settings.config"),
        )

    def output_settings_as_dict(
        self,
        checkbox_option1_state,
        checkbox_option2_state,
        label_keyboard_shortcuts_option1_content,
        label_keyboard_shortcuts_option2_content,
        label_keyboard_shortcuts_option3_content,
        label_keyboard_shortcuts_option4_content,
        label_keyboard_shortcuts_option5_content,
        combo_box_program_language_text,
    ):
        """Generate from settings inside settings dialog dict."""

        if checkbox_option1_state is True:
            checkbox_option1_state == "true"
        elif checkbox_option1_state is False:
            checkbox_option1_state == "false"

        if checkbox_option2_state is True:
            checkbox_option2_state == "true"
        elif checkbox_option2_state is False:
            checkbox_option2_state == "false"

        return {
            "programLanguage": combo_box_program_language_text,
            "openURLautomatically": checkbox_option1_state,
            "copyURLtoClipboard": checkbox_option2_state,
            "keyboardShortcuts": [
                {
                    "importNewPlaylist": label_keyboard_shortcuts_option1_content,
                    "exportPlaylist": label_keyboard_shortcuts_option2_content,
                    "clearPlaylist": label_keyboard_shortcuts_option3_content,
                    "generatePlaylist": label_keyboard_shortcuts_option4_content,
                    "shufflePlaylist": label_keyboard_shortcuts_option5_content,
                }
            ],
        }

    def act_settings(self):
        """Open settings dialog."""
        settings_dict = Ui.get_settings(self)
        dlg = SettingsDialog(self)
        Ui.load_settings(self, settings_dict)

        if dlg.exec():
            checkbox_option1_state = dlg.checkBox_option1.isChecked()
            checkbox_option2_state = dlg.checkBox_option2.isChecked()

            label_keyboard_shortcuts_option1_content = (
                dlg.label_keyboard_shortcuts_option1.text()
            )
            label_keyboard_shortcuts_option2_content = (
                dlg.label_keyboard_shortcuts_option2.text()
            )
            label_keyboard_shortcuts_option3_content = (
                dlg.label_keyboard_shortcuts_option3.text()
            )
            label_keyboard_shortcuts_option4_content = (
                dlg.label_keyboard_shortcuts_option4.text()
            )
            label_keyboard_shortcuts_option5_content = (
                dlg.label_keyboard_shortcuts_option5.text()
            )

            combo_box_program_language_text = dlg.comboBox_language.currentText()

            logging.debug(f"Option 1: {checkbox_option1_state}")
            logging.debug(f"Option 2: {checkbox_option2_state}")
            logging.debug(
                f"Keyboard Shortcut 1: {label_keyboard_shortcuts_option1_content}"
            )
            logging.debug(
                f"Keyboard Shortcut 2: {label_keyboard_shortcuts_option2_content}"
            )
            logging.debug(
                f"Keyboard Shortcut 3: {label_keyboard_shortcuts_option3_content}"
            )
            logging.debug(
                f"Keyboard Shortcut 4: {label_keyboard_shortcuts_option4_content}"
            )
            logging.debug(
                f"Keyboard Shortcut 5: {label_keyboard_shortcuts_option5_content}"
            )
            logging.debug(f"Program language: {combo_box_program_language_text}")

            settings_dict = Ui.output_settings_as_dict(
                self,
                checkbox_option1_state,
                checkbox_option2_state,
                label_keyboard_shortcuts_option1_content,
                label_keyboard_shortcuts_option2_content,
                label_keyboard_shortcuts_option3_content,
                label_keyboard_shortcuts_option4_content,
                label_keyboard_shortcuts_option5_content,
                combo_box_program_language_text,
            )
            Ui.save_settings_to_conf_file(self, settings_dict)


class ListBoxWidget(Ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        Ui.listWidget_playlist_items.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()

            print(event.mimeData().urls())

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))

                ytplaylist_dict = Ui.read_json_file(self, url.path())
                Ui.import_from_dict(self, ytplaylist_dict)
            # self.addItems(links)
        else:
            event.ignore()


class AskPlaylistResetDialog(QDialog):
    """
    Class for the dialog to ask if the playlist should be deleted with all its components.
    """

    def __init__(self, parent=None):
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


class AskPlaylistImport(QDialog):
    """
    Class for the dialog to ask if you want to create a new playlist
    or if you want to add the imported playlist to the existing playlist.
    """

    def __init__(self, parent=None):
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


class InfoDialog(QDialog):
    """
    Class for the info dialog.
    """

    def __init__(self, parent=None):
        """Load info_dialog.ui file."""
        super().__init__(parent)
        uic.loadUi((app_context.get_resource("forms/info_dialog.ui")), self)
        self.setWindowIcon(QIcon(app_context.get_resource("icon/youtube-play.icns")))
        self.setFont(QFont("Roboto"))


class SettingsDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, parent=None):
        """Load settings_dialog.ui file and connect components to their functions."""
        super().__init__(parent)
        uic.loadUi(
            app_context.get_resource("forms/settings_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource("icon/youtube-play.icns")))
        self.setFont(QFont("Roboto"))
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

    def change_button_option1_clicked(self):
        """Get text from keySequenceEdit1 field and display in label."""
        if self.keySequenceEdit_option1.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option1.setText(
                self.keySequenceEdit_option1.keySequence().toString()
            )

    def change_button_option2_clicked(self):
        """Get text from keySequenceEdit2 field and display in label."""
        if self.keySequenceEdit_option2.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option2.setText(
                self.keySequenceEdit_option2.keySequence().toString()
            )

    def change_button_option3_clicked(self):
        """Get text from keySequenceEdit3 field and display in label."""
        if self.keySequenceEdit_option3.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option3.setText(
                self.keySequenceEdit_option3.keySequence().toString()
            )

    def change_button_option4_clicked(self):
        """Get text from keySequenceEdit4 field and display in label."""
        if self.keySequenceEdit_option4.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option4.setText(
                self.keySequenceEdit_option4.keySequence().toString()
            )

    def change_button_option5_clicked(self):
        """Get text from keySequenceEdit5 field and display in label."""
        if self.keySequenceEdit_option5.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option5.setText(
                self.keySequenceEdit_option5.keySequence().toString()
            )


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

    apply_stylesheet(app, theme=app_context.get_resource("theme/yt-dark-red.xml"))

    window = Ui()
    window.show()

    exit_code = app_context.app.exec()
    sys.exit(exit_code)
