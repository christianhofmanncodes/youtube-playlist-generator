import os
import sys
import webbrowser
import ssl
import json
from urllib import request
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
    QRadioButton,
)
from qt_material import apply_stylesheet

basedir = os.path.dirname(__file__)


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(f"{os.path.join(basedir, 'forms', 'form.ui')}", self)
        self.pushButton_add.clicked.connect(self.add_button_pressed)
        self.pushButton_copy.clicked.connect(self.copy_button_pressed)
        self.pushButton_import.clicked.connect(self.import_button_pressed)
        self.pushButton_export.clicked.connect(self.export_button_pressed)
        self.pushButton_generate.clicked.connect(self.generate_button_pressed)
        self.pushButton_delete_item.clicked.connect(self.delete_item_button_clicked)
        self.pushButton_clear_playlist.clicked.connect(
            self.clear_playlist_button_clicked
        )
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.double_clicked)
        self.label_credits.linkActivated.connect(self.credits_label_clicked)

    def double_clicked(self, item):
        listwidget = self.listWidget_playlist_items
        for index in range(listwidget.count()):
            item = listwidget.item(index)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        Ui.make_item_editable(self)

    def make_item_editable(self):
        index = self.listWidget_playlist_items.currentIndex()
        if index.isValid():
            item = self.listWidget_playlist_items.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.listWidget_playlist_items.edit(index)

    def add_button_pressed(self):
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
            self.pushButton_clear_playlist.setEnabled(True)
            self.pushButton_delete_item.setEnabled(True)
            if Ui.playlist_widget_has_enough_items(self):
                self.pushButton_generate.setEnabled(True)

    def is_string_valid_url(self, string):
        if "http://" in string or "https://" in string:
            return True

    def is_string_valid_youtube_url(self, string):
        if "watch?" in string or "be/" in string:
            return True

    def cut_url_to_id(self, url):
        if "v=" in url:
            get_id = url.split("v=")
        elif "be/" in url:
            get_id = url.split("be/")
        return get_id[-1]

    def playlist_widget_has_enough_items(self):
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        if len(playlist_items) >= 2:
            return True

    def is_playlist_widget_empty(self):
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        if not playlist_items:
            return True

    def disable_delete_clear_generate_buttons(self):
        self.pushButton_clear_playlist.setEnabled(False)
        self.pushButton_delete_item.setEnabled(False)
        self.pushButton_generate.setEnabled(False)

    def clear_playlist_button_clicked(self):
        dlg = AskClearDialog(self)
        if dlg.exec():
            self.listWidget_playlist_items.clear()
            if Ui.is_playlist_widget_empty(self):
                Ui.disable_delete_clear_generate_buttons(self)
                self.pushButton_copy.setEnabled(False)
                self.textEdit_playlist_title.clear()
        else:
            print("No item was deleted!")

    def delete_item_button_clicked(self):
        list_items = self.listWidget_playlist_items.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listWidget_playlist_items.takeItem(
                self.listWidget_playlist_items.row(item)
            )
        if Ui.is_playlist_widget_empty(self):
            Ui.disable_delete_clear_generate_buttons(self)
        elif not Ui.playlist_widget_has_enough_items(self):
            self.pushButton_generate.setEnabled(False)

    def has_textedit_playlist_generated_url_content(self):
        if self.textEdit_playlist_generated_url.toPlainText() != "":
            return True

    def copy_button_pressed(self):
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def read_json_file(self, filename):
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
        return data

    def import_from_dict(self, ytplaylist_dict):
        playlist_title = ytplaylist_dict["playlistTitle"]
        playlist_ids = ytplaylist_dict["playlistIDs"]

        self.textEdit_playlist_title.setText(playlist_title)
        print(playlist_ids)
        self.listWidget_playlist_items.addItems(playlist_ids)

    def import_button_pressed(self):
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
                self.pushButton_clear_playlist.setEnabled(True)
                self.pushButton_delete_item.setEnabled(True)
                self.pushButton_generate.setEnabled(True)
        except FileNotFoundError:
            print("No file was imported.")

    def export_ytplaylist_file(self, filename, ytplaylist_dict):
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(ytplaylist_dict, file, indent=4)

    def generate_dict_from_fields(self, playlist_title, playlist_ids):
        return {"playlistTitle": playlist_title, "playlistIDs": playlist_ids}

    def output_list_from_playlist_ids(self):
        playlist = self.listWidget_playlist_items
        return [playlist.item(x).text() for x in range(playlist.count())]

    def export_button_pressed(self):
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
        if self.textEdit_playlist_title.toPlainText() == "":
            dlg = AskEmptyPlaylistTitle(self)
            if dlg.exec():
                Ui.generate_playlist(self)
        else:
            Ui.generate_playlist(self)

    def generate_playlist(self):
        self.textEdit_playlist_generated_url.setText("Playlist is being generated...")

        if Ui.has_textedit_playlist_generated_url_content(self):
            self.pushButton_copy.setEnabled(True)
            playlist = self.listWidget_playlist_items
            playlist_items = [playlist.item(x).text() for x in range(playlist.count())]
            print(playlist_items)

            comma_seperated_string = Ui.create_comma_seperated_string(
                self, playlist_items
            )
            Ui.generate_video_ids_url(self, comma_seperated_string)

    def create_comma_seperated_string(self, content_list):
        return ",".join(content_list)

    def generate_video_ids_url(self, comma_seperated_string):
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
        if " " in title:
            return True

    def replace_space_in_title(self, title_with_space):
        return title_with_space.replace(" ", "%20")

    def create_playlist_url_with_title(self, video_ids, playlist_title):
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"

    def create_playlist_url_without_title(self, video_ids):
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"

    def generate_playlist_url(self, video_ids_url):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            response = request.urlopen(video_ids_url)

            playlist_link = response.geturl()
            playlist_link = playlist_link.split("list=")[1]

            return (
                f"https://www.youtube.com/playlist?list={playlist_link}"
                + "&disable_polymer=true"
            )
        except IndexError:
            ErrorCreatingURLDialog(self).exec()
            return ""

    def open_url_in_webbrowser(self, url):
        print(f"\nOpening {url} in new Web browser tab...\n")
        webbrowser.open_new_tab(url)

    def open_playlist_url_in_webbrowser(self, playlist_url):
        Ui.open_url_in_webbrowser(self, playlist_url)

    def save_settings_to_conf_file(self, settings_dict):
        with open(
            f"{os.path.join(basedir, 'config', 'settings.config')}",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(settings_dict, file, indent=4)

    def get_settings(self):
        return Ui.read_json_file(
            self, f"{os.path.join(basedir, 'config', 'settings.config')}"
        )

    def load_settings(self, settings_dict):
        program_language = settings_dict["programLanguage"]
        open_url_automatically = settings_dict["openURLautomatically"]
        copy_url_toclipboard = settings_dict["copyURLtoclipboard"]

        shortcut_import_new_playlist = settings_dict["keyboardShortcuts"][0][
            "importNewPlaylist"
        ]
        shortcut_export_playlist = settings_dict["keyboardShortcuts"][0][
            "exportPlaylist"
        ]
        shortcut_clear_playlist = settings_dict["keyboardShortcuts"][0]["clearPlaylist"]
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

        if copy_url_toclipboard is True:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_toclipboard is False:
            SettingsDialog(self).checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        SettingsDialog(self).keySequenceEdit_option1.setKeySequence(
            shortcut_import_new_playlist
        )

        SettingsDialog(self).keySequenceEdit_option2.setKeySequence(
            shortcut_export_playlist
        )

        SettingsDialog(self).keySequenceEdit_option3.setKeySequence(
            shortcut_clear_playlist
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
            "copyURLtoclipboard": checkbox_option2_state,
            "keyboardShortcuts": [
                {
                    "importNewPlaylist": key_sequence_option1_content,
                    "exportPlaylist": key_sequence_option2_content,
                    "clearPlaylist": key_sequence_option3_content,
                    "generatePlaylist": key_sequence_option4_content,
                }
            ],
        }

    def credits_label_clicked(self):
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


class AskClearDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Are you sure?")
        self.setFixedSize(450, 140)

        q_btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(
            "Do you really want to clear your playlist? That deletes all of your items!"
        )
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class ErrorCreatingURLDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error with creating playlist URL.")
        self.setFixedSize(450, 120)

        q_btn = QDialogButtonBox.StandardButton.Ok

        self.button_box = QDialogButtonBox(q_btn)
        self.button_box.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(
            "There was an error with creating the playlist url. \nCheck if all video ids are valid and correct."
        )
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class AskEmptyPlaylistTitle(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Your playlist title is currently empty")
        self.setFixedSize(450, 140)

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
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(f"{os.path.join(basedir, 'forms', 'info_dialog.ui')}", self)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(f"{os.path.join(basedir, 'forms', 'settings_dialog.ui')}", self)
        self.pushButton_info.clicked.connect(self.info_button_pressed)

    def info_button_pressed(self):
        dlg = InfoDialog(self)
        dlg.exec()


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_red.xml")
    window = Ui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
