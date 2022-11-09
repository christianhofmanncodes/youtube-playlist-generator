"""module menu.menu"""

import logging

from actions import actions
from dialogs import import_playlist
from dialogs.dialogs import show_error_dialog
from file.file import check_file_format, read_json_file
from playlist.playlist import check_if_items_in_playlist, import_from_dict
from PyQt6.QtGui import QAction, QKeySequence
from settings import operations
from settings.settings import RECENT_FILES_STRING, SETTING_FILE_LOCATION


def get_menu_config(app_context) -> dict:
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
    The function returns a list with all the text from each action in self.menuOpen_recent,
    which is ordered by most recent first.

    :param self: Used to Access the attributes and methods of the parent class.
    :return: A list containing the text of all actions in the recent files menu.
    """
    return [action.text() for action in self.menuOpen_recent.actions()[::-1]]


def add_clear_recent_files_action_to_menu(self, app) -> None:
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
        self.menuOpen_recent.addSeparator()
        self.action = QAction()
        self.action.setText(app.translate("Menu", RECENT_FILES_STRING))
        self.menuOpen_recent.addAction(self.action)


def load_recent_files(self, app, app_context) -> None:
    """
    The load_recent_files function adds items to the recent files menu.

    :param self: Used to Access the class attributes.
    :return: None.
    """
    menu_config = get_menu_config(app_context)

    if menu_config["recent_files"]:
        file_names = menu_config["recent_files"]
        logging.debug(file_names)
        for file_name in file_names:
            add_recent_filename(self, app, file_name)
        add_clear_recent_files_action_to_menu(self, app)

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


def add_recent_filename(self, app, filename) -> None:
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
        menu_actions = self.menuOpen_recent.actions()
        before_action = menu_actions[0] if menu_actions else None
        self.menuOpen_recent.insertAction(before_action, filename_action)
        add_clear_recent_files_action_to_menu(self, app)
    else:
        logging.info("'%s' already exists in recent files menu.", filename)


def open_ytplaylist_file_from_menu(self, action, app_context) -> None:
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
                dlg = import_playlist.PlaylistImportDialog(app_context)
                if dlg.exec():
                    import_from_dict(self, ytplaylist_dict)
                else:
                    actions.act_new(self, app_context)
                    import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()
                self.menuOpen_recent.addSeparator()
                self.new_action = QAction()
                self.new_action.setText(RECENT_FILES_STRING)
                self.menuOpen_recent.addAction(self.new_action)
            else:
                import_from_dict(self, ytplaylist_dict)
                self.lineEdit_url_id.setFocus()
            actions.enable_components(self)
        else:
            show_error_dialog(
                self,
                "File not found!",
                f"File '{filename}' not found!\n\nMaybe it was deleted?",
            )

            self.menuOpen_recent.removeAction(action)
    else:
        show_error_dialog(
            self,
            "Wrong file format!",
            f"File '{filename}' is not a valid 'ytplaylist' file!",
        )

        self.menuOpen_recent.removeAction(action)


def apply_shortcuts_to_actions(self, app_context):
    """If settings differ from the default settings, apply shortcuts to actions."""
    if operations.check_if_settings_not_default(self, app_context):
        settings_dict = operations.get_settings(SETTING_FILE_LOCATION, app_context)
        self.actionNew.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["newPlaylist"])
        )
        self.actionOpen.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["openPlaylist"])
        )
        self.actionSave.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["savePlaylist"])
        )
        self.actionAdd_item.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["addItem"])
        )
        self.actionDelete_Item.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["deleteItem"])
        )
        self.actionRename_item.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["renameItem"])
        )
        self.actionShuffle.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["shufflePlaylist"])
        )
        self.actionGenerate_Playlist.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["generatePlaylist"])
        )
        self.actionCount_items.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["countItems"])
        )
        self.actionClear_all_items.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["clearAllItems"])
        )
        self.actionGet_video_information.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["getVideoInformation"])
        )
        self.actionRemove_duplicates.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["removeDuplicates"])
        )
        self.actionCopy_URL.setShortcut(
            QKeySequence(settings_dict["keyboard_shortcuts"][0]["copyURL"])
        )
