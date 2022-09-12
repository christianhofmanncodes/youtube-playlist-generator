"""module actions.actions"""

import logging

from dialogs.dialogs import (
    show_error_dialog,
    show_info_dialog,
    show_question_dialog,
)
from dialogs.settings_dialog import SettingsDialog
from dialogs import reset_playlist
from file.file import read_json_file
from menu import menu
from playlist import playlist
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QMessageBox
from settings.operations import (
    get_settings,
    output_settings_as_dict,
    save_settings_to_conf_file,
)
from settings.settings import APP_VERSION, RELEASE_DATE
from url import open_url
from strings import check_string


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


def process_filename(self, action):
    """Import YouTube Playlist file (*.ytplaylist)"""
    menu.open_ytplaylist_file_from_menu(self, action)


@pyqtSlot(QAction)
def act_recent_file(self, action):
    """Action for click on one recent file."""
    if action.text() == "Clear recent files":
        actions = self.recent_files_menu.actions()
        for action_to_remove in actions:
            self.recent_files_menu.removeAction(action_to_remove)
    else:
        process_filename(self, action)


def act_new(self) -> None:
    """
    Creates a blank state to start a new playlist.
    If the playlist already contains items and should be deleted
    remove all items in playlist and disable all buttons
    and clear playlist title field.
    """
    if playlist.playlist_widget_has_x_or_more_items(self, 1):
        dlg = reset_playlist.PlaylistResetDialog()
        if dlg.exec():
            self.listWidget_playlist_items.clear()
            logging.debug("Playlist was reset successfully.")
            if playlist.is_playlist_widget_empty(self):
                disable_components(self)
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
        if playlist.is_playlist_widget_empty(self):
            disable_components(self)
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
    show_info_dialog(self, "Success!", "All items in playlist deleted successfully.")
    if playlist.is_playlist_widget_empty(self):
        disable_components(self)
        self.pushButton_copy.setEnabled(False)
        self.actionCopy_URL.setEnabled(False)
        self.lineEdit_url_id.setFocus()

    if not playlist.playlist_widget_has_x_or_more_items(self, 1):
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
    if self.lineEdit_url_id.text():
        self.pushButton_add.setEnabled(True)
        self.actionAdd_item.setEnabled(True)
    else:
        self.pushButton_add.setEnabled(False)
        self.actionAdd_item.setEnabled(False)


def act_shuffle(self):
    """Shuffle playlist items."""
    playlist.shuffle(self)


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
    playlist.make_item_editable(self)


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

        if playlist.playlist_widget_has_x_or_more_items(self, 1):
            self.actionClear_all_items.setEnabled(True)

        if playlist.playlist_widget_has_x_or_more_items(self, 2):
            self.pushButton_generate.setEnabled(True)
            self.actionGenerate_Playlist.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.actionRemove_duplicates.setEnabled(True)
            self.menuSort_items.setEnabled(True)
            self.actionAscending.setEnabled(True)
            self.actionDescending.setEnabled(True)

        if playlist.playlist_widget_has_x_or_more_items(self, 3):
            self.pushButton_shuffle_playlist.setEnabled(True)
            self.actionShuffle.setEnabled(True)


def act_remove_duplicates(self) -> None:
    """Check if two or more items in playlist. Remove duplicates."""
    if playlist.playlist_widget_has_x_or_more_items(self, 2):
        playlist.remove_duplicates_from_playlist(self)


def act_delete_item(self) -> [None, bool]:
    """If item selected delete it from the playlist."""
    list_items = self.listWidget_playlist_items.selectedItems()
    if not list_items:
        return
    for item in list_items:
        self.listWidget_playlist_items.takeItem(
            self.listWidget_playlist_items.row(item)
        )
    if playlist.is_playlist_widget_empty(self):
        disable_components(self)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 1):
        self.actionClear_all_items.setEnabled(False)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 2):
        self.pushButton_generate.setEnabled(False)
        self.actionGenerate_Playlist.setEnabled(False)
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionRemove_duplicates.setEnabled(False)
        self.menuSort_items.setEnabled(False)
        self.actionAscending.setEnabled(False)
        self.actionDescending.setEnabled(False)
        self.actionClear_all_items.setEnabled(False)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 3):
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionShuffle.setEnabled(False)


def act_copy_url(self) -> None:
    """Get content from textEdit_playlist_generated_url and copy it to clipboard."""
    text = self.textEdit_playlist_generated_url.toPlainText()
    QApplication.clipboard().setText(text)


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
            if playlist.check_if_items_in_playlist(self):
                logging.debug("There are already items in playlist!")
                dlg = import_playlist.PlaylistImportDialog()

                if dlg.exec():
                    playlist.import_from_dict(self, ytplaylist_dict)
                else:
                    act_new(self)
                    playlist.import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()
            else:
                playlist.import_from_dict(self, ytplaylist_dict)
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
            menu.add_recent_filename(self, filename[0])
    except FileNotFoundError:
        logging.error("File not found. No file was imported.")


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
            ytplaylist_dict = self.generate_dict_from_fields(
                self,
                self.lineEdit_playlist_title.text(),
                self.output_list_from_playlist_ids(self),
            )
            self.export_ytplaylist_file(self, filename[0], ytplaylist_dict)
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
            playlist.generate_playlist(self)
    else:
        playlist.generate_playlist(self)


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
            "shortcut_6": dlg.label_keyboard_shortcuts_option6.text(),
            "shortcut_7": dlg.label_keyboard_shortcuts_option7.text(),
            "shortcut_8": dlg.label_keyboard_shortcuts_option8.text(),
            "shortcut_9": dlg.label_keyboard_shortcuts_option9.text(),
            "shortcut_10": dlg.label_keyboard_shortcuts_option10.text(),
            "shortcut_11": dlg.label_keyboard_shortcuts_option11.text(),
            "shortcut_12": dlg.label_keyboard_shortcuts_option12.text(),
        }

        logging.debug(components_dict)
        settings_dict = output_settings_as_dict(components_dict)
        save_settings_to_conf_file(settings_dict)
