"""module actions.actions"""

import logging

from dialogs import import_playlist, reset_playlist
from dialogs.dialogs import show_info_dialog, show_question_dialog
from dialogs.settings_dialog import SettingsDialog
from file import file
from file.file import read_json_file
from menu.menu import add_recent_filename, open_ytplaylist_file_from_menu
from playlist import playlist, video_info
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QMessageBox
from settings.operations import (
    get_settings,
    output_settings_as_dict,
    save_settings_to_conf_file,
)
from settings.settings import (
    APP_VERSION,
    RECENT_FILES_STRING,
    RELEASE_DATE,
    SETTING_FILE_LOCATION,
)
from strings import check_string
from url import open_url
from url.url import cut_url_to_id


def disable_components(self) -> None:
    """
    The disable_components function disables specific components.

    :param self: Used to Access the class attributes.
    :return: None.
    """
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
    self.actionCount_items.setEnabled(False)
    self.actionGet_video_information.setEnabled(False)
    self.actionClear_all_items.setEnabled(False)
    self.actionRemove_duplicates.setEnabled(False)
    self.textEdit_playlist_generated_url.setEnabled(False)
    self.actionAscending.setEnabled(False)
    self.actionDescending.setEnabled(False)


def process_filename(self, action):
    """
    The process_filename function imports a YouTube Playlist file (*.ytplaylist)
    and creates a new playlist.

    :param self: Used to Access the attributes and methods of the class MainWindow.
    :param action: Used to Pass the menu action to the function.
    :return: The filename of the youtube playlist file that was imported.
    """
    open_ytplaylist_file_from_menu(self, action)


@pyqtSlot(QAction)
def act_recent_file(self, action):
    """
    The act_recent_file function is a function that is called when the user clicks
    on one of the recent files in the recent files menu. It takes as input an action,
    which is a QAction object. If the action's text is RECENT_FILES_STRING,
    then it removes all actions from self.recent_files_menu and then adds them back in
    (except for RECENT_FILES_STRING).
    Otherwise, it calls the process_filename function with that file name.

    :param self: Used to Access the variables and methods of the class.
    :param action: Used to Identify the action that has been clicked.
    :return: The action that is clicked on.
    """
    if action.text() == RECENT_FILES_STRING:
        actions = self.recent_files_menu.actions()
        for action_to_remove in actions:
            self.recent_files_menu.removeAction(action_to_remove)
    else:
        process_filename(self, action)


def act_new(self) -> None:
    """
    The act_new function creates a blank state to start a new playlist.
    If the playlist already contains items and should be deleted,
    it removes all items in playlist and disables all buttons
    and finally clears playlist title field.

    :param self: Used to Access the components of the MainWindow.
    :return: None.
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


def act_undo() -> None:
    """
    The act_undo function undoes the last change.

    :return: None.
    """
    print("Undo...")


def act_redo() -> None:
    """
    The act_redo function redoes the last change.

    :return: None.
    """
    print("Redo...")


def act_cut() -> None:
    """
    The act_cut function cuts text from selected text field.

    :return: None.
    """
    print("Cut...")


def act_copy() -> None:
    """
    The act_copy function copies text from selected text field.

    :return: None.
    """
    print("Copy...")


def act_paste() -> None:
    """
    The act_paste function pastes text to the selected text field.

    :return: None.
    """
    print("Paste...")


def act_select_all() -> None:
    """
    The act_select_all function selects all text from the selected text field.

    :return: None.
    """
    print("Select all...")


def act_find(self) -> None:
    """
    The act_find function finds text in the playlist.

    :param self: Used to Access the widgets and other properties of the MainWindow class.
    :return: None.
    """
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
    """
    The act_count_items function displays the number of items in the playlist.
    It opens a dialog box and displays a message with the number of items in
    the playlist.

    :param self: Used to Access the attributes and methods of the class in which it is used.
    :return: A message box that displays the number of items in the playlist.
    """
    QMessageBox.information(
        self,
        "Info",
        f"Number of items in playlist: {self.listWidget_playlist_items.count()}",
    )


def act_clear_items(self) -> None:
    """
    The act_clear_items function clears all items in the playlist.
    This is not the reset function!

    :param self: Used to Access the class variables.
    :return: None.
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
        self.actionGet_video_information.setEnabled(False)


def act_sort_items_ascending(self) -> None:
    """
    The act_sort_items_ascending function sorts the items in the playlist
    in ascending order. The function is called when the user clicks on the 'Ascending'
    entry in the menu located under "Sort items".

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    self.listWidget_playlist_items.setSortingEnabled(True)
    self.listWidget_playlist_items.sortItems(Qt.SortOrder.AscendingOrder)
    self.listWidget_playlist_items.setSortingEnabled(False)


def act_sort_items_descending(self) -> None:
    """
    The act_sort_items_descending function sorts the items in the playlist list widget
    in descending order. The function is called when the user clicks on the 'Descending'
    entry in the menu located under "Sort items".

    :param self: Used to Access the variables, methods and signals of the class.
    :return: None.
    """
    self.listWidget_playlist_items.setSortingEnabled(True)
    self.listWidget_playlist_items.sortItems(Qt.SortOrder.DescendingOrder)
    self.listWidget_playlist_items.setSortingEnabled(False)


def act_url_id_text_change(self) -> None:
    """
    The act_url_id_text_change function enables the Add button only
    if the lineEdit_url_id is not empty.

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    if self.lineEdit_url_id.text():
        self.pushButton_add.setEnabled(True)
        self.actionAdd_item.setEnabled(True)
    else:
        self.pushButton_add.setEnabled(False)
        self.actionAdd_item.setEnabled(False)


def act_shuffle(self):
    """
    The act_shuffle function shuffles the playlist items.

    :param self: Used to Access the class instance inside of a method.
    :return: A list of shuffled playlist items.
    """
    playlist.shuffle(self)


def act_about(self) -> QMessageBox:
    """
    The act_about function executes a QMessageBox with the title "About YouTube Playlist Generator"
    and the version number and release date of that version as text.

    :param self: Used to Access the attributes and methods of the class.
    :return: A QMessagebox.
    """
    return QMessageBox.about(
        self,
        "About YouTube Playlist Generator",
        f"""YouTube Playlist Generator by Christian Hofmann\n
        Version {APP_VERSION} ({RELEASE_DATE})""",
    )


def act_about_qt(self) -> QMessageBox:
    """
    The act_about_qt function executes the About QMessageBox.

    :returns: The result of the QMessageBox.aboutQt function.

    :param self: Used to Access the attributes and methods of the class.
    :return: The QMessageBox.
    """
    return QMessageBox.aboutQt(self)


def act_license(self) -> QMessageBox:
    """
    The act_license function executes the License Information dialog box.
    It returns a QMessageBox object.

    :param self: Used to Access the attributes and methods of the parent class.
    :return: The value of the license_dialog object.
    """
    return self.license_dialog.exec()


def act_contact() -> None:
    """
    The act_contact function opens the default mail software with the contact email address.

    :return: None.
    """
    open_url.in_webbrowser("mailto:contact@youtube-playlist-generator.com")


def act_report_a_bug() -> None:
    """
    The act_report_a_bug function opens the Github issue page from project.

    :return: None.
    """
    open_url.in_webbrowser(
        "https://github.com/christianhofmanncodes/youtube-playlist-generator/issues"
    )


def act_github() -> None:
    """
    The act_github function opens the Github page of the project in a web browser.

    :return: None.
    """
    open_url.in_webbrowser(
        "https://github.com/christianhofmanncodes/youtube-playlist-generator"
    )


def act_rename_item(self) -> None:
    """
    The act_rename_item function adds the ItemIsEditable flag to all items in the playlist.
    This allows for double clicking on an item and renaming it.

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    list_widget = self.listWidget_playlist_items
    for index in range(list_widget.count()):
        item = list_widget.item(index)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
    playlist.make_item_editable(self)


def act_add_item(self) -> None:
    """
    The act_add_item function is used to add items to the playlist.
    It first checks if the textEdit field is empty, and if it is not, then it will check
    if the string in that field is a valid URL.
    If so, then it will convert that URL into an ID and add that item to the playlist.
    Otherwise, it will just add whatever string was in there as an item.

    :param self: Used to Access the variables and methods of the class.
    :return: None.
    """
    text = self.lineEdit_url_id.text()
    if text != "":
        if check_string.is_string_valid_url(
            text
        ) and check_string.is_string_valid_youtube_url(text):
            user_id = cut_url_to_id(text)
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
            self.actionCount_items.setEnabled(True)
            self.actionClear_all_items.setEnabled(True)
            self.actionGet_video_information.setEnabled(True)

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
    """
    The act_remove_duplicates function removes duplicate items from the playlist.
    It checks if there are two or more items in the playlist, and if so, it removes duplicates.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    if playlist.playlist_widget_has_x_or_more_items(self, 2):
        playlist.remove_duplicates_from_playlist(self)


def act_delete_item(self) -> [None, bool]:
    """
    The act_delete_item function is a function that is called
    when the user clicks on the delete item button.
    It will remove any selected items from the playlist widget.

    :param self: Used to Access the components of the MainWindow class.
    :return: None.
    """
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
        self.actionCount_items.setEnabled(False)
        self.actionClear_all_items.setEnabled(False)
        self.actionGet_video_information.setEnabled(False)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 2):
        self.pushButton_generate.setEnabled(False)
        self.actionGenerate_Playlist.setEnabled(False)
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionRemove_duplicates.setEnabled(False)
        self.menuSort_items.setEnabled(False)
        self.actionAscending.setEnabled(False)
        self.actionDescending.setEnabled(False)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 3):
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionShuffle.setEnabled(False)


def act_copy_url(self) -> None:
    """
    The act_copy_url function copies the text from the textEdit_playlist_generated_url to clipboard.

    :param self: Used to Access the variables and methods of the class.
    :return: None.
    """
    text = self.textEdit_playlist_generated_url.toPlainText()
    QApplication.clipboard().setText(text)


def act_open(self) -> None:
    """
    The act_open function is called when the user clicks on the "Open" action.
    It opens a file dialog and lets the user choose a .ytplaylist-file to import.
    The function then imports that file into the program.

    :param self: Used to Access the class variables.
    :return: None.
    """
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
            self.actionCount_items.setEnabled(True)
            self.actionClear_all_items.setEnabled(True)
            self.actionGet_video_information.setEnabled(True)
            add_recent_filename(self, filename[0])
    except FileNotFoundError:
        logging.error("File not found. No file was imported.")


def act_save(self) -> None:
    """
    The act_save function is called when the user clicks on the "Save" button.
    It will open a file dialog to get a path from the user, and then generate
    a .ytplaylist-file using that path. The function will also log what happened.

    :param self: Used to Access the fields of the main window.
    :return: None.
    """
    try:
        if filename := QFileDialog.getSaveFileName(
            self,
            "Export YouTube Playlist file",
            "",
            "YouTube Playlist file (*.ytplaylist)",
        ):
            logging.debug("Playlist exported under:")
            logging.debug(filename[0])
            ytplaylist_dict = playlist.generate_dict_from_fields(
                self.lineEdit_playlist_title.text(),
                playlist.output_list_from_playlist_ids(self),
            )
            file.export_ytplaylist_file(filename[0], ytplaylist_dict)
    except FileNotFoundError:
        logging.error("Error during export process! No file was exported.")


def act_generate(self) -> None:
    """
    The act_generate function checks if the playlist title is empty. If it is,
    it asks the user if they want to proceed. If not, it proceeds with generating
    the playlist URL.

    :param self: Used to Access the class variables.
    :return: None.
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
    """
    The act_settings function opens the settings dialog.
    The user can change the language, theme, and keyboard shortcuts.
    The function saves these changes to a configuration file.

    :param self: Used to Access the attributes and methods of the class in which it is used.
    :return: None.
    """
    settings_dict = get_settings(SETTING_FILE_LOCATION)
    dlg = SettingsDialog(self)
    dlg.load_settings(settings_dict)

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
            "shortcut_13": dlg.label_keyboard_shortcuts_option13.text(),
        }

        logging.debug(components_dict)
        settings_dict = output_settings_as_dict(components_dict)
        save_settings_to_conf_file(settings_dict, SETTING_FILE_LOCATION)


def act_video_information(self) -> None:
    """
    The act_video_information function displays the video title of the selected item in playlist.
    If no item is selected, a warning message box appears.

    :param self: Used to Access the class attributes.
    :return: The video title and the channel name of the selected item in playlist.
    """
    try:
        video_id = self.listWidget_playlist_items.currentItem().text()
        if video_title_channel := video_info.get_title__channel_from_youtube_link(
            video_id
        ):
            QMessageBox.information(self, "Video information", video_title_channel)
        else:
            QMessageBox.critical(
                self,
                "Error while fetching video information",
                f"The id '{video_id}' is invalid.",
            )
    except AttributeError as attribute_error:
        QMessageBox.critical(
            self,
            "Error while fetching video information",
            "No item in playlist selected.",
        )
        logging.warning(attribute_error)
