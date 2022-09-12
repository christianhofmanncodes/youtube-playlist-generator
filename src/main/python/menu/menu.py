"""module menu.menu"""

import logging

# from actions.actions import act_new #FIXME: Throws Cyclic import
from dialogs import import_playlist
from dialogs.dialogs import show_error_dialog
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file import file
from playlist import playlist
from PyQt6.QtGui import QAction
from settings.settings import RECENT_FILES_STRING

app_context = ApplicationContext()


def get_menu_config() -> list:
    """Return content from menu.config."""
    return file.read_json_file(
        app_context.get_resource("config/menu.config"),
    )


def get_recent_files_items_menu(self) -> list:
    """Return list with recent files from menu"""
    return [action.text() for action in self.recent_files_menu.actions()[::-1]]


def delete_unnecessary_entries_recent_file_menu(self) -> None:
    """Delete empty entries and Clear recent files items."""
    recent_files = get_recent_files_items_menu(self)
    while "" in recent_files:
        recent_files.remove("")
    while RECENT_FILES_STRING in recent_files:
        recent_files.remove(RECENT_FILES_STRING)


def load_recent_files(self) -> None:
    """Add items to recent files."""
    menu_config = get_menu_config()

    if menu_config["recent_files"]:
        file_names = menu_config["recent_files"]
        logging.debug(file_names)
        for file_name in file_names:
            add_recent_filename(self, file_name)
        self.recent_files_menu.addSeparator()
        self.action = QAction()
        self.action.setText(RECENT_FILES_STRING)
        self.recent_files_menu.addAction(self.action)
    else:
        logging.info("No recent files!")
        delete_unnecessary_entries_recent_file_menu(self)


def add_recent_filename(self, filename):
    """Add filename to recent file menu."""
    filename_action = QAction(filename, self)
    actions = self.recent_files_menu.actions()
    before_action = actions[0] if actions else None
    self.recent_files_menu.insertAction(before_action, filename_action)


def open_ytplaylist_file_from_menu(self, action):
    """Open *.ytplaylist file from recent files menu."""
    filename = action.text()
    ytplaylist_dict = file.read_json_file(filename)
    if file.check_file_format(filename, ".ytplaylist"):
        if ytplaylist_dict:
            logging.debug("Playlist to be imported:")
            logging.debug(ytplaylist_dict)
            if playlist.check_if_items_in_playlist(self):
                logging.debug("There are already items in playlist!")
                dlg = import_playlist.PlaylistImportDialog()
                if dlg.exec():
                    playlist.import_from_dict(self, ytplaylist_dict)
                else:
                    # act_new(self)
                    playlist.import_from_dict(self, ytplaylist_dict)
                    self.lineEdit_url_id.setFocus()
                self.recent_files_menu.addSeparator()
                self.new_action = QAction()
                self.new_action.setText(RECENT_FILES_STRING)
                self.recent_files_menu.addAction(self.new_action)
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
