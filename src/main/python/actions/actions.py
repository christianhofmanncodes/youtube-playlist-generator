"""module actions.actions"""

import logging
from typing import List, Literal, Tuple, Union

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QInputDialog,
    QMessageBox,
)

from dialogs import import_playlist, reset_playlist
from dialogs.builtin_dialogs import show_info_dialog, show_question_dialog
from dialogs.search_dialog import SearchDialog
from dialogs.settings_dialog import SettingsDialog
from dialogs.video_info_dialog import VideoInfoDialog
from file import file
from file.file import read_csv_file, read_json_file, read_txt_file
from menu.menu import (
    add_recent_filename,
    apply_shortcuts_to_actions,
    open_ytplaylist_file_from_menu,
)
from playlist import playlist, video_info
from settings.operations import (
    check_if_language_was_changed,
    get_settings,
    output_settings_as_dict,
    save_settings_to_conf_file,
)
from settings.settings import (
    APP_VERSION,
    FILE_NOT_FOUND_STRING,
    RECENT_FILES_STRING,
    RELEASE_DATE,
    SETTING_FILE_LOCATION,
)
from strings import check_string, replace_string
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
    self.actionExport.setEnabled(False)
    self.actionReset_Playlist.setEnabled(False)
    self.actionDelete_Item.setEnabled(False)
    self.actionGenerate_Playlist.setEnabled(False)
    self.actionShuffle.setEnabled(False)
    self.actionRename_item.setEnabled(False)
    self.actionSave.setEnabled(False)
    self.actionSave_as.setEnabled(False)
    self.actionRemove_duplicates.setEnabled(False)
    self.actionCount_items.setEnabled(False)
    self.menuSort_items.setEnabled(True)
    self.actionClear_all_items.setEnabled(False)
    self.actionGet_video_information.setEnabled(False)
    self.textEdit_playlist_generated_url.setEnabled(False)
    self.actionAscending.setEnabled(False)
    self.actionDescending.setEnabled(False)


def enable_components(self) -> None:
    """
    The enable_components function enables specific components.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    self.pushButton_new.setEnabled(True)
    self.pushButton_generate.setEnabled(True)
    self.pushButton_shuffle_playlist.setEnabled(True)
    self.actionExport.setEnabled(True)
    self.actionReset_Playlist.setEnabled(True)
    self.actionGenerate_Playlist.setEnabled(True)
    self.actionShuffle.setEnabled(True)
    self.actionSave.setEnabled(True)
    self.actionSave_as.setEnabled(True)
    self.actionRemove_duplicates.setEnabled(True)
    self.actionCount_items.setEnabled(True)
    self.menuSort_items.setEnabled(True)
    self.actionClear_all_items.setEnabled(True)
    self.actionAscending.setEnabled(True)
    self.actionDescending.setEnabled(True)


def process_filename(self, action, app_context):
    """
    The process_filename function imports a YouTube Playlist file (*.ytplaylist)
    and creates a new playlist.

    :param self: Used to Access the attributes and methods of the class MainWindow.
    :param action: Used to Pass the menu action to the function.
    :return: The filename of the youtube playlist file that was imported.
    """
    open_ytplaylist_file_from_menu(self, action, app_context)


@pyqtSlot(QAction)
def act_recent_file(self, app_context, action) -> None:
    """
    The act_recent_file function is a function that is called when the user clicks
    on one of the recent files in the recent files menu. It takes as input an action,
    which is a QAction object. If the action's text is RECENT_FILES_STRING,
    then it removes all actions from self.menuOpen_recent and then adds them back in
    (except for RECENT_FILES_STRING).
    Otherwise, it calls the process_filename function with that file name.

    :param self: Used to Access the variables and methods of the class.
    :param action: Used to Identify the action that has been clicked.
    :return: The action that is clicked on.
    """
    if action.text() == RECENT_FILES_STRING:
        actions = self.menuOpen_recent.actions()
        for action_to_remove in actions:
            self.menuOpen_recent.removeAction(action_to_remove)
    else:
        process_filename(self, action, app_context)
        logging.info("Imported file: %s successfully.", action.text())


def act_new(self, app_context) -> None:
    """
    The act_new function creates a blank state to start a new playlist.
    If the playlist already contains items and should be deleted,
    it removes all items in playlist and disables all buttons
    and finally clears playlist title field.

    :param self: Used to Access the components of the MainWindow.
    :return: None.
    """
    if playlist.playlist_widget_has_x_or_more_items(self, 1):
        dlg = reset_playlist.PlaylistResetDialog(app_context)
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
                self.statusBar.clearMessage()
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
            self.statusBar.clearMessage()


def act_undo(self) -> None:
    """
    The act_undo function undoes the last change.

    :return: None.
    """
    if self.lineEdit_playlist_title.hasFocus():
        self.lineEdit_playlist_title.undo()
    elif self.lineEdit_url_id.hasFocus():
        self.lineEdit_url_id.undo()


def act_redo(self) -> None:
    """
    The act_redo function redoes the last change.

    :return: None.
    """
    if self.lineEdit_playlist_title.hasFocus():
        self.lineEdit_playlist_title.redo()
    elif self.lineEdit_url_id.hasFocus():
        self.lineEdit_url_id.redo()


def act_cut(self) -> None:
    """
    The act_cut function cuts text from selected text field.

    :return: None.
    """
    if self.lineEdit_playlist_title.hasSelectedText():
        self.lineEdit_playlist_title.cut()
    elif self.lineEdit_url_id.hasSelectedText():
        self.lineEdit_url_id.cut()


def act_copy(self) -> None:
    """
    The act_copy function copies text from selected text field.

    :return: None.
    """
    if self.lineEdit_playlist_title.hasSelectedText():
        self.lineEdit_playlist_title.copy()
    elif self.lineEdit_url_id.hasSelectedText():
        self.lineEdit_url_id.copy()


def act_paste(self) -> None:
    """
    The act_paste function pastes text to the selected text field.

    :return: None.
    """
    if self.lineEdit_playlist_title.hasFocus():
        self.lineEdit_playlist_title.paste()
    elif self.lineEdit_url_id.hasFocus():
        self.lineEdit_url_id.paste()


def act_select_all(self) -> None:
    """
    The act_select_all function selects all text from the selected text field.

    :return: None.
    """
    if (
        self.lineEdit_playlist_title.text() != ""
        and self.lineEdit_playlist_title.hasFocus()
    ):
        self.lineEdit_playlist_title.selectAll()
    elif self.lineEdit_url_id.text() != "" and self.lineEdit_url_id.hasFocus():
        self.lineEdit_url_id.selectAll()


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
    self.actionSave.setEnabled(True)


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
    self.actionSave.setEnabled(True)


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


def act_click_playlist_item(self) -> None:
    """
    The act_click_playlist_item function enables or disables
    specific components based on selection in the playlist.

    :param self: Used to Access the class attributes and methods.
    :return: None.
    """
    if not self.listWidget_playlist_items.selectedItems():
        self.pushButton_delete_item.setEnabled(False)
        self.actionDelete_Item.setEnabled(False)
        self.actionRename_item.setEnabled(False)
        self.actionGet_video_information.setEnabled(False)
    else:
        self.pushButton_delete_item.setEnabled(True)
        self.actionDelete_Item.setEnabled(True)
        self.actionRename_item.setEnabled(True)
        self.actionGet_video_information.setEnabled(True)


def act_shuffle(self):
    """
    The act_shuffle function shuffles the playlist items.

    :param self: Used to Access the class instance inside of a method.
    :return: A list of shuffled playlist items.
    """
    playlist.shuffle(self)
    self.actionSave.setEnabled(True)


def act_about(self):
    """
    The act_about function executes a QMessageBox with the title "About YouTube Playlist Generator"
    and the version number and release date of that version as text.

    :param self: Used to Access the attributes and methods of the class.
    :return: A QMessagebox.
    """
    return QMessageBox.about(
        self,
        "About YouTube Playlist Generator",
        (
            "YouTube Playlist Generator\nby Christian Hofmann\n"
            f"\nVersion {APP_VERSION} ({RELEASE_DATE})"
        ),
    )


def act_about_qt(self):
    """
    The act_about_qt function executes the About QMessageBox.

    :returns: The result of the QMessageBox.aboutQt function.

    :param self: Used to Access the attributes and methods of the class.
    :return: The QMessageBox.
    """
    return QMessageBox.aboutQt(self)


def act_license(self):
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
    self.actionSave.setEnabled(True)


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
            if user_id != "":
                self.listWidget_playlist_items.addItem(str(user_id))

            item = self.listWidget_playlist_items.findItems(
                user_id, Qt.MatchFlag.MatchRegularExpression
            )[0]

        elif check_string.is_string_valid_url(
            text
        ) and check_string.is_string_playlist_url(text):
            playlist_items = video_info.get_playlist_items(text)

            cut_ids_playlist_items = [
                cut_url_to_id(playlist_item) for playlist_item in playlist_items
            ]

            self.listWidget_playlist_items.addItems(cut_ids_playlist_items)

            item = self.listWidget_playlist_items.findItems(
                cut_ids_playlist_items[-1], Qt.MatchFlag.MatchRegularExpression
            )[0]

        else:
            self.listWidget_playlist_items.addItem(str(text))

            item = self.listWidget_playlist_items.findItems(
                text, Qt.MatchFlag.MatchRegularExpression
            )[0]

        item.setSelected(True)
        self.listWidget_playlist_items.scrollToItem(item)
        enable_components_after_add_act(self)


def enable_components_after_add_act(self) -> None:
    """
    The enable_components_after_add_act function enables the following components:
        - The lineEdit_url_id component.
        - The pushButton_new component.
        - The actionReset_Playlist action.
        - The actionSave action.

       If the playlist widget has 1 or more items, then it enables the following components:
            *The Count Items menu item under Tools menu item.*

            *The Clear All Items menu item under Tools menu item.*

       If the playlist widget has 2 or more items, then it enables the following components:
            *The Generate Playlist button.*

            *The Generate Playlist menu item under File Menu Item*

            *The Save As... menu Item*

       If there are 3 or more items in a playlist, then it enables these two actions/components:
            *The Shuffle menu Item*

            *The pushButton_shuffle_playlist component*

    :param self: Used to Access the class attributes and methods.
    :return: None.
    """
    self.lineEdit_url_id.clear()
    self.pushButton_new.setEnabled(True)
    self.actionReset_Playlist.setEnabled(True)
    self.actionSave.setEnabled(True)

    if playlist.playlist_widget_has_x_or_more_items(self, 1):
        self.actionCount_items.setEnabled(True)
        self.actionClear_all_items.setEnabled(True)

    if playlist.playlist_widget_has_x_or_more_items(self, 2):
        self.pushButton_generate.setEnabled(True)
        self.actionGenerate_Playlist.setEnabled(True)
        self.actionSave.setEnabled(True)
        self.actionSave_as.setEnabled(True)
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


def act_delete_item(self) -> Union[bool, None]:
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
    self.actionSave.setEnabled(True)
    if playlist.is_playlist_widget_empty(self):
        disable_components(self)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 1):
        self.actionCount_items.setEnabled(False)
        self.actionClear_all_items.setEnabled(False)

    elif not playlist.playlist_widget_has_x_or_more_items(self, 2):
        self.pushButton_generate.setEnabled(False)
        self.actionGenerate_Playlist.setEnabled(False)
        self.pushButton_shuffle_playlist.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionSave_as.setEnabled(False)
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


def act_open(self, app, app_context) -> None:
    """
    The act_open function is called when the user clicks on the "Open" action.
    It opens a file dialog and lets the user choose a .ytplaylist-file to import.
    The function then imports that file into the program.
    If the playlist already contains items, the user will be prompted to choose
    if he wants to add them or create a new playlist.

    :param self: Used to Access the class variables.
    :return: None.
    """
    try:
        filename = QFileDialog.getOpenFileName(
            self,
            "Import YouTube Playlist file",
            "",
            "YouTube Playlist file (*.ytplaylist)",
        )
    except FileNotFoundError:
        logging.error(FILE_NOT_FOUND_STRING)
        filename = ""
    if filename[0] != "":
        open_ytplaylist_file(self, app, app_context, filename[0])


def open_ytplaylist_file(self, app, app_context, filename: str) -> None:
    """
    The open_ytplaylist_file function opens a .ytplaylist file containing
    a list of YouTube video IDs. The function then adds the videos to the playlist
    and enables components such as buttons etc.

    :param self: Used to Access the class variables.
    :param app_context: Used to Pass the QApplication object to the dialog.
    :param filename: Used to Store the filename of the playlist that is imported.
    :return: None.
    """
    ytplaylist_dict = read_json_file(filename)
    logging.debug("Playlist to be opened:")
    logging.debug(ytplaylist_dict)
    if playlist.check_if_items_in_playlist(self):
        logging.debug("There are already items in playlist!")
        dlg = import_playlist.PlaylistImportDialog(app_context)

        if dlg.exec():
            playlist.import_from_dict(self, ytplaylist_dict)
        else:
            act_new(self, app_context)
            playlist.import_from_dict(self, ytplaylist_dict)
            self.lineEdit_url_id.setFocus()
    else:
        logging.debug("Playlist is empty.")
        playlist.import_from_dict(self, ytplaylist_dict)
        self.lineEdit_url_id.setFocus()
    enable_components(self)
    add_recent_filename(self, app, filename)
    self.statusBar.showMessage(filename, 0)


def get_list_of_strings(filename: Tuple[str, str] | Literal[""]) -> List[str]:
    """
    The get_list_of_strings function takes a tuple of strings as input.
    The first string is the filename, and the second string is the filetype.
    If it's a text file, read_txt_file() will be called to get a list of strings from that file.
    If it's a CSV file, read_csv_file() will be called to get a list of strings from that file.

    :param filename:tuple[str: Used to Pass the filename to the function.
    :param str]: Used to Specify the type of file that is being read.
    :return: The list of strings from the file that was chosen by the user.
    """
    if filename[1] == "Text file (*.txt)":
        return read_txt_file(filename[0])
    return read_csv_file(filename[0]) if filename[1] == "CSV file (*.csv)" else []


def replace_empty_strings_in_list(list_of_strings: List) -> List:
    """
    The replace_empty_strings_in_list function removes empty strings from a list of strings.

    :param list_of_strings:list: Used to Specify the list of strings that will be processed.
    :return: A list of strings with all empty strings removed.
    """
    return (
        replace_string.remove_empty_strings_in_list(list_of_strings)
        if list_of_strings
        else []
    )


def create_video_ids_list(list_of_strings: List) -> List:
    """
    The create_video_ids_list function takes a list of strings
    and returns a new list with the same elements,
    except that any string which is not a valid YouTube URL
    will be converted to its corresponding video ID.

    :param list_of_strings:list: Used to Pass a list of strings to the function.
    :return: A list of video ids from a list of strings.
    """
    video_ids_list = []
    for item in list_of_strings:
        if check_string.is_string_valid_url(
            item
        ) and check_string.is_string_valid_youtube_url(item):
            video_id = cut_url_to_id(item)
            video_ids_list.append(video_id)
        else:
            video_ids_list.append(item)
    return video_ids_list


def generate_dict_from_video_ids_list(video_ids_list: List) -> dict:
    """
    The generate_dict_from_video_ids_list function takes a list of video IDs
    and returns a dictionary with the video IDs as keys and empty strings as values.
    This is useful for creating an initial playlist dictionary, which
    will be used to create the final playlist.

    :param video_ids_list:list: Used to Pass a list of video ids to the function.
    :return: A dictionary with the video_ids as keys and empty strings as values.
    """
    return playlist.generate_dict_from_fields("", video_ids_list)


def import_items_into_playlist(self, app_context, ytplaylist_dict: dict) -> None:
    """
    The import_items_into_playlist function is used to import a playlist into the current playlist.
    It checks if there are any items in the current playlist, and if so it prompts the user
    with a dialog box asking them if they want to replace all of those items or not.
    If they do, then it replaces all of those items with new ones from the imported file.
    If not, then it creates a new empty list and imports only that list.

    :param self: Used to Access the class variables.
    :param app_context: Used to Pass the QApplication object.
    :param ytplaylist_dict:dict: Used to Import the playlist into the GUI.
    :return: None.
    """
    if playlist.check_if_items_in_playlist(self):
        logging.debug("There are already items in playlist!")
        dlg = import_playlist.PlaylistImportDialog(app_context)

        if dlg.exec():
            playlist.import_from_dict(self, ytplaylist_dict)
        else:
            act_new(self, app_context)
            playlist.import_from_dict(self, ytplaylist_dict)
            self.lineEdit_playlist_title.setFocus()
    else:
        logging.debug("Playlist is empty.")
        playlist.import_from_dict(self, ytplaylist_dict)
        self.lineEdit_playlist_title.setFocus()
    enable_components(self)
    # add_recent_filename(self, filename[0])


def import_txt_or_csv_file(
    self, app_context, filename: Tuple[str, str] | Literal[""]
) -> None:
    """
    The import_txt_or_csv_file function imports a list of video IDs or URLs from a text file,
    CSV file, or URL into the current playlist. The function checks if there are any items
    in the playlist already and displays an error message if so. If not, it imports the list
    of video IDs/URLs into the current playlist.

    :param self: Used to Access the fields of the MainWindow class.
    :param app_context: Used to Pass the QApplication object to the dialog.
    :param filename: Used to Store the path to the file.
    :return: None
    """
    list_of_strings = get_list_of_strings(filename)
    list_of_strings = replace_empty_strings_in_list(list_of_strings)
    video_ids_list = create_video_ids_list(list_of_strings)
    ytplaylist_dict = generate_dict_from_video_ids_list(video_ids_list)
    import_items_into_playlist(self, app_context, ytplaylist_dict)


def act_import(self, app_context) -> None:
    """
    The act_import function is called when the user clicks on the "Import" button.
    It opens a file dialog and lets the user choose a .txt-file to import.
    The function then imports that file into the program.
    If the playlist already contains items, the user will be prompted to choose
    if he wants to add them or create a new playlist.

    :param self: Used to Access the class variables.
    :return: None.
    """
    try:
        filename = QFileDialog.getOpenFileName(
            self,
            "Import Text or CSV file",
            "",
            "Text file (*.txt);;CSV file (*.csv)",
        )
    except FileNotFoundError:
        logging.error(FILE_NOT_FOUND_STRING)
        filename = ""
    if filename[0] != "":
        import_txt_or_csv_file(self, app_context, filename)


def act_export(self) -> None:
    """
    The act_export function is called when the user clicks on the "Export" button.
    It opens a file dialog and lets the user choose a location to either
    export a .txt file or a .csv file.
    The function then exports the playlist items to the chosen destination.

    :param self: Used to Access the class variables.
    :return: None.
    """
    video_ids_list = playlist.output_list_from_playlist_ids(self)
    try:
        filename = QFileDialog.getSaveFileName(
            self,
            "Export Text or CSV file",
            "",
            "Text file (*.txt);;CSV file (*.csv)",
        )
    except FileNotFoundError:
        logging.error(FILE_NOT_FOUND_STRING)
        filename = ""
    if filename[1] == "Text file (*.txt)":
        file.write_txt_file(filename[0], video_ids_list)
    elif filename[1] == "CSV file (*.csv)":
        file.write_csv_file(filename[0], video_ids_list)


def act_save(self) -> None:
    """
    The act_save function saves the current playlist to a file.
    The filename is taken from the status bar, and it's contents are generated
    from the current playlist. The function also disables saving until another
    playlist is loaded.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    filename = self.statusBar.currentMessage()
    ytplaylist_dict = playlist.generate_dict_from_fields(
        self.lineEdit_playlist_title.text(),
        playlist.output_list_from_playlist_ids(self),
    )
    file.export_ytplaylist_file(filename, ytplaylist_dict)
    self.actionSave.setEnabled(False)


def act_save_as(self) -> None:
    """
    The act_save_as function is called when the user clicks on the "Save as..." button.
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
            logging.debug("Playlist saved under:")
            logging.debug(filename[0])
            ytplaylist_dict = playlist.generate_dict_from_fields(
                self.lineEdit_playlist_title.text(),
                playlist.output_list_from_playlist_ids(self),
            )
            file.export_ytplaylist_file(filename[0], ytplaylist_dict)
    except FileNotFoundError:
        logging.error("Error during process! No file was saved.")


def act_generate(self, app_context) -> None:
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
            generate_playlist_url(self, app_context)
    else:
        generate_playlist_url(self, app_context)


def generate_playlist_url(self, app_context) -> None:
    """
    The generate_playlist_url function generates a playlist url.
    It then displays the generated playlist url in the text edit box
    and shows an info dialog to let the user know that it was successful.
    It also outputs the playlist duration.

    :param self: Used to Access the class attributes.
    :param app_context: Used to Pass the app object to the function.
    :return: None.
    """
    self.textEdit_playlist_generated_url.setText("")
    self.textEdit_playlist_generated_url.setEnabled(False)
    self.pushButton_copy.setEnabled(False)
    playlist.generate_playlist(self, app_context)
    playlist_url = self.textEdit_playlist_generated_url.toPlainText()
    if playlist_url != "":
        self.statusBar.showMessage(
            (
                "Playlist length for generated playlist: "
                f"{video_info.get_playlist_length(playlist_url)}"
            ),
            0,
        )


def act_settings(self, app, app_context) -> None:
    """
    The act_settings function opens the settings dialog.
    The user can change the language, theme, and keyboard shortcuts.
    The function saves these changes to a configuration file.

    :param self: Used to Access the attributes and methods of the class in which it is used.
    :return: None.
    """
    settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)
    dlg = SettingsDialog(app, app_context)
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
        else:
            radio_button_theme = "normal"

        components_dict = {
            "option_1": dlg.checkBox_option1.isChecked(),
            "option_2": dlg.checkBox_option2.isChecked(),
            "language": dlg.comboBox_language.currentText(),
            "theme": radio_button_theme,
            "shortcut_1": dlg.tableWidget.item(0, 2).text(),
            "shortcut_2": dlg.tableWidget.item(1, 2).text(),
            "shortcut_3": dlg.tableWidget.item(2, 2).text(),
            "shortcut_4": dlg.tableWidget.item(3, 2).text(),
            "shortcut_5": dlg.tableWidget.item(4, 2).text(),
            "shortcut_6": dlg.tableWidget.item(5, 2).text(),
            "shortcut_7": dlg.tableWidget.item(6, 2).text(),
            "shortcut_8": dlg.tableWidget.item(7, 2).text(),
            "shortcut_9": dlg.tableWidget.item(8, 2).text(),
            "shortcut_10": dlg.tableWidget.item(9, 2).text(),
            "shortcut_11": dlg.tableWidget.item(10, 2).text(),
            "shortcut_12": dlg.tableWidget.item(11, 2).text(),
            "shortcut_13": dlg.tableWidget.item(12, 2).text(),
            "shortcut_14": dlg.tableWidget.item(13, 2).text(),
            "shortcut_15": dlg.tableWidget.item(14, 2).text(),
            "shortcut_16": dlg.tableWidget.item(15, 2).text(),
            "shortcut_17": dlg.tableWidget.item(16, 2).text(),
            "shortcut_18": dlg.tableWidget.item(17, 2).text(),
            "shortcut_19": dlg.tableWidget.item(18, 2).text(),
        }

        logging.debug(components_dict)
        settings_dict = output_settings_as_dict(components_dict)
        apply_shortcuts_to_actions(self, app_context)
        selected_language = dlg.comboBox_language.currentText()

        if check_if_language_was_changed(self, app_context, selected_language):
            save_settings_to_conf_file(
                settings_dict, SETTING_FILE_LOCATION, app_context
            )
            SettingsDialog.restart_if_confirmed(self, app, app_context)
        else:
            save_settings_to_conf_file(
                settings_dict, SETTING_FILE_LOCATION, app_context
            )


def act_video_information(self, app, app_context) -> None:
    """
    The act_video_information function is called when the user clicks on "Get video information".
    It will open a dialog window with information about that specific video.

    :param self: Used to Access the class attributes.
    :param app: Used to Access the application instance.
    :param app_context: Used to Pass the QApplication instance to the dialog.
    :return: None.
    """
    try:
        video_id = self.listWidget_playlist_items.currentItem().text()
    except AttributeError:
        QMessageBox.critical(
            self,
            "Error while fetching video information",
            "Please select an item in the playlist.",
        )
        logging.warning("No item in playlist selected.")
        video_id = ""

    if video_id != "":
        if video_information := video_info.get_video_info(video_id):
            dlg = VideoInfoDialog(app, app_context, video_information)
            if dlg.exec():
                logging.info("VideInfoDialog successfully opened.")
        else:
            QMessageBox.critical(
                self,
                "Error while fetching video information",
                f"The id '{video_id}' is invalid.",
            )


def act_search_videos(self, app_context):
    """
    The act_search_videos function is called when the user clicks
    on the "Search" button in the SearchDialog.
    The results are displayed in a table widget with checkboxes next to each row.
    The user can select one or more rows
    and click "Add Selected Videos" to add them to their playlist.

    :param self: Used to Refer to the current instance of the class.
    :param app: Used to Pass the QApplication instance to the SearchDialog class.
    :param app_context: Used to Pass the application context to the SearchDialog class.
    :return: A list of video_ids that are checked in the search results dialog.
    """
    dlg = SearchDialog(app_context)
    if dlg.exec():
        logging.info("SearchDialog successfully opened.")

        if dlg.search_object and dlg.search_results is not None:
            checked_list = [
                dlg.tableWidget_search_results.item(index, 11).text()
                for index in range(dlg.tableWidget_search_results.rowCount())
                if (
                    dlg.tableWidget_search_results.item(index, 0).checkState()
                    == Qt.CheckState.Checked
                )
            ]
            for video_id in checked_list:
                self.listWidget_playlist_items.addItem(str(video_id))

                item = self.listWidget_playlist_items.findItems(
                    video_id, Qt.MatchFlag.MatchRegularExpression
                )[0]

                item.setSelected(True)
                self.listWidget_playlist_items.scrollToItem(item)

            enable_components_after_add_act(self)
