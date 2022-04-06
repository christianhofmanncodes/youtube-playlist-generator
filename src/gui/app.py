"""app module"""

import contextlib
import json
import os
import random
import ssl
import sys
import webbrowser
from urllib import error, request

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QVBoxLayout,
)
from qt_material import apply_stylesheet


BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.join(os.path.dirname(__file__), "..")
ROOT_DIR = os.path.extsep

with contextlib.suppress(ImportError):
    from ctypes import windll  # Only exists on Windows.

    APP_ID = "christianhofmann.youtube-playlist-generator.gui.0.0.4"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Ui(QMainWindow):
    """
    Class for the main window with all its components and functions.
    """

    def __init__(self):
        """Connect UI components with specific functions."""
        super(Ui, self).__init__()
        uic.loadUi(f"{os.path.join(BASE_DIR, 'forms', 'form.ui')}", self)
        self.setFont(QFont("Roboto"))
        self.pushButton_add.clicked.connect(self.add_button_pressed)
        self.actionAdd_item.triggered.connect(self.add_button_pressed)
        self.pushButton_copy.clicked.connect(self.copy_button_pressed)
        self.actionCopy_URL.triggered.connect(self.copy_button_pressed)
        self.actionImport.triggered.connect(self.import_button_pressed)
        self.actionExport.triggered.connect(self.export_button_pressed)
        self.pushButton_generate.clicked.connect(self.generate_button_pressed)
        self.actionGenerate_Playlist.triggered.connect(self.generate_button_pressed)
        self.pushButton_delete_item.clicked.connect(self.delete_item_button_clicked)
        self.actionDelete_Item.triggered.connect(self.delete_item_button_clicked)
        self.pushButton_reset_playlist.clicked.connect(
            self.reset_playlist_button_clicked
        )
        self.pushButton_shuffle_playlist.clicked.connect(self.shuffle_clicked)
        self.actionReset_Playlist.triggered.connect(self.reset_playlist_button_clicked)
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.double_clicked)
        self.actionRename_item.triggered.connect(self.double_clicked)
        self.actionSettings.triggered.connect(self.settings_clicked)
        self.actionGithub.triggered.connect(self.github_clicked)
        self.actionReport_a_bug.triggered.connect(self.report_a_bug)
        self.actionContact.triggered.connect(self.contact)
        self.actionAbout.triggered.connect(self.info_button_pressed)
        self.actionShuffle.triggered.connect(self.shuffle_clicked)
        self.textEdit_url_id.textChanged.connect(self.url_id_text_changed)
        self.actionQuit.triggered.connect(self.quit)
        self.textEdit_url_id.setFocus()

    def quit(self):
        """Quits the application."""
        sys.exit()

    def url_id_text_changed(self):
        """Enable Add button only if textEdit_url_id is not empty."""
        if self.textEdit_url_id.toPlainText() != "":
            self.pushButton_add.setEnabled(True)
            self.actionAdd_item.setEnabled(True)
        else:
            self.pushButton_add.setEnabled(False)
            self.actionAdd_item.setEnabled(False)

    def shuffle_clicked(self):
        """Shuffle playlist with random.shuffle()."""
        print("Shuffle playlist...")
        playlist = Ui.output_list_from_playlist_ids(self)
        random.shuffle(playlist)
        print(playlist)

        ytplaylist_dict = Ui.generate_dict_from_fields(
            self,
            self.textEdit_playlist_title.toPlainText(),
            playlist,
        )

        print(ytplaylist_dict)
        self.listWidget_playlist_items.clear()
        Ui.import_from_dict(self, ytplaylist_dict)

    def info_button_pressed(self):
        """Execute InfoDialog."""
        dlg = InfoDialog(self)
        dlg.exec()

    def contact(self):
        """Open default mail software with contact email address."""
        self.open_url_in_webbrowser("mailto:contact@youtube-playlist-generator.com")

    def report_a_bug(self):
        """Open Github issue page from project."""
        self.open_url_in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator/issues"
        )

    def github_clicked(self):
        """Open Github page from project."""
        self.open_url_in_webbrowser(
            "https://github.com/christianhofmanncodes/youtube-playlist-generator"
        )

    def double_clicked(self, item):
        """Add flag ItemIsEditable to double clicked item in playlist."""
        listwidget = self.listWidget_playlist_items
        for index in range(listwidget.count()):
            item = listwidget.item(index)
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

    def add_button_pressed(self):
        """
        Get content from textEdit field and convert URL to ID if necessary.
        Otherwise add new item to playlist.
        """
        text = self.textEdit_url_id.toPlainText()
        if text != "":
            if Ui.is_string_valid_url(self, text) and Ui.is_string_valid_youtube_url(
                self, text
            ):
                user_id = Ui.cut_url_to_id(self, text)
                self.listWidget_playlist_items.addItem(str(user_id))
            else:
                self.listWidget_playlist_items.addItem(str(text))
                # self.listWidget_playlist_items.scrollToItem(item)
            self.textEdit_url_id.clear()
            self.pushButton_reset_playlist.setEnabled(True)
            self.pushButton_delete_item.setEnabled(True)
            self.actionDelete_Item.setEnabled(True)
            self.actionRename_item.setEnabled(True)
            self.actionReset_Playlist.setEnabled(True)
            if Ui.playlist_widget_has_enough_items(self):
                self.pushButton_generate.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionExport.setEnabled(True)

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

    def playlist_widget_has_enough_items(self):
        """Return True if two ore more items in playlist."""
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        return len(playlist_items) >= 2

    def is_playlist_widget_empty(self):
        """Return True if no items in the playlist."""
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        return not playlist_items

    def disable_components(self):
        """Disable specific components."""
        self.pushButton_reset_playlist.setEnabled(False)
        self.pushButton_delete_item.setEnabled(False)
        self.pushButton_generate.setEnabled(False)
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionReset_Playlist.setEnabled(False)
        self.actionDelete_Item.setEnabled(False)
        self.actionGenerate_Playlist.setEnabled(False)
        self.actionShuffle.setEnabled(False)
        self.actionRename_item.setEnabled(False)
        self.actionExport.setEnabled(False)

    def reset_playlist_button_clicked(self):
        """
        If playlist should be deleted remove all items in playlist and disable all buttons
        and clear playlist title field.
        """
        dlg = AskPlaylistResetDialog(self)
        if dlg.exec():
            self.listWidget_playlist_items.clear()
            if Ui.is_playlist_widget_empty(self):
                Ui.disable_components(self)
                self.pushButton_copy.setEnabled(False)
                self.actionCopy_URL.setEnabled(False)
                self.textEdit_playlist_title.clear()
                self.textEdit_url_id.setFocus()
        else:
            print("No item was deleted!")

    def delete_item_button_clicked(self):
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
        elif not Ui.playlist_widget_has_enough_items(self):
            self.pushButton_generate.setEnabled(False)
            self.actionGenerate_Playlist.setEnabled(False)
            self.actionShuffle.setEnabled(False)
            self.pushButton_shuffle_playlist.setEnabled(False)
            self.actionExport.setEnabled(False)

    def has_textedit_playlist_generated_url_content(self):
        """Return True if textEdit_playlist_generated_url is not empty."""
        return self.textEdit_playlist_generated_url.toPlainText() != ""

    def copy_button_pressed(self):
        """Get content from textEdit_playlist_generated_url and copy it to clipboard."""
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def read_json_file(self, filename):
        """Return content from json-file."""
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
        return data

    def import_from_dict(self, ytplaylist_dict):
        """Get content from dict and show it inside the application."""
        playlist_title = ytplaylist_dict["playlistTitle"]
        playlist_ids = ytplaylist_dict["playlistIDs"]

        self.textEdit_playlist_title.setText(playlist_title)
        print(playlist_ids)
        self.listWidget_playlist_items.addItems(playlist_ids)

    def import_button_pressed(self):
        """Get path of .ytplaylist-file and import it via import_from_dict()."""
        try:
            if filename := QFileDialog.getOpenFileName(
                self,
                "Import YouTube Playlist file",
                "",
                "YouTube Playlist file (*.ytplaylist)",
            ):
                ytplaylist_dict = Ui.read_json_file(self, filename[0])
                print(ytplaylist_dict)
                Ui.import_from_dict(self, ytplaylist_dict)
                self.pushButton_reset_playlist.setEnabled(True)
                self.pushButton_delete_item.setEnabled(True)
                self.pushButton_generate.setEnabled(True)
                self.pushButton_shuffle_playlist.setEnabled(True)
                self.actionReset_Playlist.setEnabled(True)
                self.actionDelete_Item.setEnabled(True)
                self.actionGenerate_Playlist.setEnabled(True)
                self.actionShuffle.setEnabled(True)
                self.actionRename_item.setEnabled(True)
                self.actionExport.setEnabled(True)
        except FileNotFoundError:
            print("No file was imported.")

    def export_ytplaylist_file(self, filename, ytplaylist_dict):
        """Write playlist title and playlist items from dict to given filename.ytplaylist-file."""
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(ytplaylist_dict, file, indent=4)

    def generate_dict_from_fields(self, playlist_title, playlist_ids):
        """Return playlist items and title as dict."""
        return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}

    def output_list_from_playlist_ids(self):
        """Return playlist items as a list."""
        playlist = self.listWidget_playlist_items
        return [playlist.item(x).text() for x in range(playlist.count())]

    def export_button_pressed(self):
        """Get path to save .ytplaylist-file and generate file."""
        try:
            if filename := QFileDialog.getSaveFileName(
                self,
                "Export YouTube Playlist file",
                "",
                "YouTube Playlist file (*.ytplaylist)",
            ):
                print(filename[0])
                ytplaylist_dict = Ui.generate_dict_from_fields(
                    self,
                    self.textEdit_playlist_title.toPlainText(),
                    Ui.output_list_from_playlist_ids(self),  # NEEDS TO BE CHANGED
                )
                Ui.export_ytplaylist_file(self, filename[0], ytplaylist_dict)
        except FileNotFoundError:
            print("No file was exported.")

    def generate_button_pressed(self):
        """
        Check if playlist title empty, ask if it should be added.
        Otherwise generate playlist URL.
        """
        if self.textEdit_playlist_title.toPlainText() == "":
            dlg = AskEmptyPlaylistTitle(self)
            if dlg.exec():
                Ui.generate_playlist(self)
        else:
            Ui.generate_playlist(self)

    def generate_playlist(self):
        """Generate playlist URL and enable copy button."""
        self.textEdit_playlist_generated_url.setText("Playlist is being generated...")

        if Ui.has_textedit_playlist_generated_url_content(self):
            self.pushButton_copy.setEnabled(True)
            self.actionCopy_URL.setEnabled(True)
            playlist = self.listWidget_playlist_items
            playlist_items = [playlist.item(x).text() for x in range(playlist.count())]
            print(playlist_items)

            comma_seperated_string = Ui.create_comma_seperated_string(
                self, playlist_items
            )
            Ui.generate_video_ids_url(self, comma_seperated_string)

    def create_comma_seperated_string(self, content_list):
        """Add commas after each item from list and return it as a string."""
        return ",".join(content_list)

    def generate_video_ids_url(self, comma_seperated_string):
        """Generate the video ids URL from a comma seperated string."""
        if self.textEdit_playlist_title.toPlainText() == "":
            video_ids_url = Ui.create_playlist_url_without_title(
                self, comma_seperated_string
            )

        elif Ui.has_space_in_title(self, self.textEdit_playlist_title.toPlainText()):
            title_no_spaces = Ui.replace_space_in_title(
                self, self.textEdit_playlist_title.toPlainText()
            )
            video_ids_url = Ui.create_playlist_url_with_title(
                self, comma_seperated_string, title_no_spaces
            )
        else:
            video_ids_url = Ui.create_playlist_url_with_title(
                self, comma_seperated_string, self.textEdit_playlist_title.toPlainText()
            )
        playlist_url = self.generate_playlist_url(video_ids_url)
        if playlist_url != "":
            self.textEdit_playlist_generated_url.setText(playlist_url)
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
        except IndexError:
            ErrorCreatingURLDialog(self).exec()
            return ""
        except error.URLError as url_error:
            ErrorCreatingURLDialog(self).exec()
            print(url_error)
            return ""

    def open_url_in_webbrowser(self, url):
        """Open a URL in Webbrowser in a new tab."""
        print(f"\nOpening {url} in new Web browser tab...\n")
        webbrowser.open_new_tab(url)

    def open_playlist_url_in_webbrowser(self, playlist_url):
        """Open the generated playlist URL in Webbrowser."""
        Ui.open_url_in_webbrowser(self, playlist_url)

    def save_settings_to_conf_file(self, settings_dict):
        """Write content from dict to settings.config."""
        with open(
            f"{os.path.join(BASE_DIR, 'config', 'settings.config')}",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(settings_dict, file, indent=4)

    def get_settings(self):
        """Return content from settings.config."""
        return Ui.read_json_file(
            self, f"{os.path.join(BASE_DIR, 'config', 'settings.config')}"
        )

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
        if program_language == "English":
            SettingsDialog(self).comboBox_language.setCurrentIndex(0)
        elif program_language == "Deutsch":
            SettingsDialog(self).comboBox_language.setCurrentIndex(1)

        if open_url_automatically is True:
            SettingsDialog(self).checkBox_option1.setCheckState(Qt.CheckState.Checked)

        elif open_url_automatically is False:
            SettingsDialog(self).checkBox_option1.setCheckState(Qt.CheckState.Unchecked)

        if copy_url_to_clipboard is True:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_to_clipboard is False:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        SettingsDialog(self).keySequenceEdit_option1.setKeySequence(
            shortcut_import_new_playlist
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

    def output_settings_as_dict(
        self,
        checkbox_option1_state,
        checkbox_option2_state,
        key_sequence_option1_content,
        key_sequence_option2_content,
        key_sequence_option3_content,
        key_sequence_option4_content,
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
                    "importNewPlaylist": key_sequence_option1_content,
                    "exportPlaylist": key_sequence_option2_content,
                    "clearPlaylist": key_sequence_option3_content,
                    "generatePlaylist": key_sequence_option4_content,
                }
            ],
        }

    def settings_clicked(self):
        """Open settings dialog."""
        settings_dict = Ui.get_settings(self)
        Ui.load_settings(self, settings_dict)
        dlg = SettingsDialog(self)

        if dlg.exec():
            checkbox_option1_state = dlg.checkBox_option1.isChecked()
            checkbox_option2_state = dlg.checkBox_option2.isChecked()

            key_sequence_option1_content = (
                dlg.keySequenceEdit_option1.keySequence().toString()
            )
            key_sequence_option2_content = (
                dlg.keySequenceEdit_option2.keySequence().toString()
            )
            key_sequence_option3_content = (
                dlg.keySequenceEdit_option3.keySequence().toString()
            )
            key_sequence_option4_content = (
                dlg.keySequenceEdit_option4.keySequence().toString()
            )

            combo_box_program_language_text = dlg.comboBox_language.currentText()

            print(f"Option 1: {checkbox_option1_state}")
            print(f"Option 2: {checkbox_option2_state}")
            print(f"Keyboard Shortcut 1: {key_sequence_option1_content}")
            print(f"Keyboard Shortcut 2: {key_sequence_option2_content}")
            print(f"Keyboard Shortcut 3: {key_sequence_option3_content}")
            print(f"Keyboard Shortcut 4: {key_sequence_option4_content}")
            print(f"Program language: {combo_box_program_language_text}")

            settings_dict = Ui.output_settings_as_dict(
                self,
                checkbox_option1_state,
                checkbox_option2_state,
                key_sequence_option1_content,
                key_sequence_option2_content,
                key_sequence_option3_content,
                key_sequence_option4_content,
                combo_box_program_language_text,
            )
            Ui.save_settings_to_conf_file(self, settings_dict)


class AskPlaylistResetDialog(QDialog):
    """
    Class for the dialog to ask if the playlist should be deleted with all its components.
    """

    def __init__(self, parent=None):
        """Build the dialog with its components."""
        super().__init__(parent)

        self.setWindowTitle("Are you sure?")
        self.setFixedSize(450, 140)
        self.setWindowIcon(
            QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns"))
        )
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


class ErrorCreatingURLDialog(QDialog):
    """
    Class for the dialog if something went wrong with the creation of the playlist URL.
    """

    def __init__(self, parent=None):
        """Build the dialog with its components."""
        super().__init__(parent)
        self.setWindowTitle("Error with creating playlist URL.")
        self.setFixedSize(450, 120)
        self.setWindowIcon(
            QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns"))
        )
        self.setFont(QFont("Roboto"))

        q_btn = QDialogButtonBox.StandardButton.Ok

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message_tuple = (
            "There was an error with creating the playlist url. \n",
            "Check if all video ids are valid and correct.",
        )
        message_text = "".join(message_tuple)
        message = QLabel(message_text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class AskEmptyPlaylistTitle(QDialog):
    """
    Class for the dialog to ask if a playlist title should be added with all its components.
    """

    def __init__(self, parent=None):
        """Build the dialog with its components."""
        super().__init__(parent)

        self.setWindowTitle("Your playlist title is currently empty")
        self.setFixedSize(450, 140)
        self.setWindowIcon(
            QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns"))
        )
        self.setFont(QFont("Roboto"))

        q_btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("There is no title for playlist yet. Do you want to proceed?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class InfoDialog(QDialog):
    """
    Class for the info dialog.
    """

    def __init__(self, parent=None):
        """Load info_dialog.ui file."""
        super().__init__(parent)
        uic.loadUi(f"{os.path.join(BASE_DIR, 'forms', 'info_dialog.ui')}", self)
        self.setWindowIcon(
            QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns"))
        )
        self.setFont(QFont("Roboto"))


class SettingsDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, parent=None):
        """Load settings_dialog.ui file and connect components to their functions."""
        super().__init__(parent)
        uic.loadUi(f"{os.path.join(BASE_DIR, 'forms', 'settings_dialog.ui')}", self)
        self.setWindowIcon(
            QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns"))
        )
        self.setFont(QFont("Roboto"))


def run():
    """Execute application and apply stylesheet."""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(ROOT_DIR, "res/icon", "youtube-play.icns")))
    apply_stylesheet(app, theme="dark_red.xml")
    window = Ui()
    window.show()
    sys.exit(app.exec())
