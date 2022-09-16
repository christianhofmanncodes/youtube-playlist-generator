"""module menu.menu"""

import logging

from actions import actions
from dialogs import import_playlist
from dialogs.dialogs import show_error_dialog
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file.file import check_file_format, read_json_file
from playlist.playlist import check_if_items_in_playlist, import_from_dict
from PyQt6.QtGui import QAction
from settings.settings import RECENT_FILES_STRING

app_context = ApplicationContext()


def get_menu_config() -> list:
    """
    The get_menu_config function returns the content from menu.config.

    :return: A list of dictionaries.
    """
    return read_json_file(
        app_context.get_resource("config/menu.config"),
    )


def get_recent_files_items_menu(self) -> list:
    """
    The get_recent_files_items_menu function returns a list of the recent files from the menu.
    The function returns a list with all the text from each action in self.recent_files_menu,
    which is ordered by most recent first.

    :param self: Used to Access the attributes and methods of the parent class.
    :return: A list containing the text of all actions in the recent files menu.
    """
    return [action.text() for action in self.recent_files_menu.actions()[::-1]]


def add_clear_recent_files_action_to_menu(self) -> None:
    """
    The add_clear_recent_files_action_to_menu function adds
    a clear recent files option to the recent files menu.

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    recent_files_items = get_recent_files_items_menu(self)
    clear_recent_files_option = any(
        item == RECENT_FILES_STRING for item in recent_files_items
    )

    if not clear_recent_files_option:
        self.recent_files_menu.addSeparator()
        self.action = QAction()
        self.action.setText(RECENT_FILES_STRING)
        self.recent_files_menu.addAction(self.action)


def load_recent_files(self) -> None:
    """
    The load_recent_files function adds items to the recent files menu.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    menu_config = get_menu_config()

    if menu_config["recent_files"]:
        file_names = menu_config["recent_files"]
        logging.debug(file_names)
        for file_name in file_names:
            add_recent_filename(self, file_name)
        add_clear_recent_files_action_to_menu(self)

    else:
        logging.info("No recent files!")


def check_if_filename_already_exist(self, filename) -> bool:
    """
    The check_if_filename_already_exist function checks
    if the filename already exist in the recent files menu.
    If it does, then it returns True, otherwise False.

    :param self: Used to Access the attributes and methods of the class.
    :param filename: Used to Check if the filename already exist in the recent files menu.
    :return: A boolean value.
    """
    all_recent_files = get_recent_files_items_menu(self)
    return filename in all_recent_files


def add_recent_filename(self, filename) -> None:
    """
    The add_recent_filename function adds a filename to the recent files menu.
    It does this by creating an action for the filename and inserting it into the menu.
    If the filename already exists in recent files, it is not added.

    :param self: Used to Access the attributes and methods of the class.
    :param filename: Used to Set the text of the action.
    :return: None.
    """
    if not check_if_filename_already_exist(self, filename):
        filename_action = QAction(filename, self)
        menu_actions = self.recent_files_menu.actions()
        before_action = menu_actions[0] if menu_actions else None
        self.recent_files_menu.insertAction(before_action, filename_action)
    else:
        logging.info("'%s' already exists in recent files menu.", filename)


def open_ytplaylist_file_from_menu(self, action) -> None:
    """
    The open_ytplaylist_file_from_menu function opens
    a *.ytplaylist file from the recent files menu.
    It checks if the file is in correct format and if it is,
    it imports its content into playlist.

    :param self: Used to Access the class variables.
    :param action: Used to Get the filename of the file that was opened.
    :return: None.
    """
    filename = action.text()
    ytplaylist_dict = read_json_file(filename)
    if check_file_format(filename, ".ytplaylist"):
        if ytplaylist_dict:
            logging.debug("Playlist to be imported:")
            logging.debug(ytplaylist_dict)
            if check_if_items_in_playlist(self):
                logging.debug("There are already items in playlist!")
                dlg = import_playlist.PlaylistImportDialog()
                if dlg.exec():
                    import_from_dict(self, ytplaylist_dict)
                else:
                    actions.act_new(self)
                    import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()
                self.recent_files_menu.addSeparator()
                self.new_action = QAction()
                self.new_action.setText(RECENT_FILES_STRING)
                self.recent_files_menu.addAction(self.new_action)
            else:
                import_from_dict(self, ytplaylist_dict)
                self.lineEdit_url_id.setFocus()
            action.enable_components(self)
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
