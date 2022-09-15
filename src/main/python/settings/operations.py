"""settings.operations module"""

import json

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file.file import read_json_file
from menu import menu
from settings.settings import RECENT_FILES_STRING

app_context = ApplicationContext()


def create_recent_file_menu(self) -> None:
    """
    The create_recent_file_menu function creates a menu that lists the most recently opened files.
    The function is called when the user clicks on "Open recent" in the File menu. The function
    connects to an event handler, which is triggered when a file from this list is clicked.

    :param self: Used to Access the variables and methods.
    :return: The recent_files_menu.
    """
    self.file_menu = self.menuFile
    self.recent_files_menu = self.file_menu.addMenu("&Open recent")
    self.recent_files_menu.triggered.connect(self.act_recent_file)


def get_settings() -> dict:
    """
    The get_settings function returns the settings.config file as a dictionary.

    :return: A dictionary.
    """
    return read_json_file(
        app_context.get_resource("config/settings.config"),
    )


def save_settings_to_conf_file(settings_dict: dict) -> None:
    """
    The save_settings_to_conf_file function writes the content of a dictionary to settings.config.

    :param settings_dict:dict: Used to Pass the settings dictionary to the save_settings_to_conf_file function.
    :return: None.
    """
    with open(
        app_context.get_resource("config/settings.config"),
        "w",
        encoding="UTF-8",
    ) as file:
        json.dump(settings_dict, file, indent=4)


def save_menu_to_conf_file(menu_dict: dict) -> None:
    """
    The save_menu_to_conf_file function writes the content of a dictionary to a file.
    The function takes one argument, menu_dict, which is the dictionary that will be written to file.

    :param menu_dict:dict: Used to Pass the menu_dict to the save_menu_to_conf_file function.
    :return: None.
    """
    with open(
        app_context.get_resource("config/menu.config"),
        "w",
        encoding="UTF-8",
    ) as file:
        json.dump(menu_dict, file, indent=4)


def output_settings_as_dict(
    components_dict: dict,
) -> dict:
    """
    The output_settings_as_dict function generates a dictionary from the settings
    inside the settings dialog. The output_settings_as_dict function takes in one argument,
    components_dict, which is a dictionary containing all of the components inside
    the SettingsDialog class. The output_settings_as_dict function returns a dictionary
    containing two keys: general and keyboard shortcuts. Each key contains another
    dictionary with each setting as its own key and value pair.

    :param components_dict:dict: Used to Pass the dictionary of settings from the settings dialog to this function.
    :param : Used to Generate the settings dict.
    :return: A dictionary with the settings that are inside the settings dialog.
    """

    """Generate from settings inside settings dialog dict."""
    return {
        "general": [
            {
                "openURLautomatically": components_dict["option_1"],
                "copyURLtoClipboard": components_dict["option_2"],
                "programLanguage": components_dict["language"],
                "appTheme": components_dict["theme"],
            },
        ],
        "keyboard_shortcuts": [
            {
                "newPlaylist": components_dict["shortcut_1"],
                "openPlaylist": components_dict["shortcut_2"],
                "savePlaylist": components_dict["shortcut_3"],
                "addItem": components_dict["shortcut_4"],
                "deleteItem": components_dict["shortcut_5"],
                "renameItem": components_dict["shortcut_6"],
                "shufflePlaylist": components_dict["shortcut_7"],
                "generatePlaylist": components_dict["shortcut_8"],
                "countItems": components_dict["shortcut_9"],
                "clearAllItems": components_dict["shortcut_10"],
                "getVideoInformation": components_dict["shortcut_11"],
                "removeDuplicates": components_dict["shortcut_12"],
                "copyURL": components_dict["shortcut_13"],
            }
        ],
    }


def output_menu_config_as_dict(recent_files: list) -> dict:
    """
    The output_menu_config_as_dict function generates a dictionary from the recent files list.
    The output_menu_config_as_dict function takes in a list of strings and returns a dictionary.

    :param recent_files:list: Used to Pass a list of recent files to the output_menu_config function.
    :return: A dictionary with a single key, "recent_files", which has a value of the recent files list.
    """
    return {"recent_files": list(recent_files)}


def load_settings(self) -> None:
    """
    The load_settings function loads the settings from menu.config into the program.

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    create_recent_file_menu(self)
    menu.load_recent_files(self)


def remove_unnecessary_entries_from_menu_dict(self, menu_dict) -> dict:
    """
    The remove_unnecessary_entries_from_menu_dict function removes the RECENT_FILES_STRING and empty strings from
    the recent files list in the menu dictionary. This is done to prevent these entries from being displayed in the
    menu bar.

    :param self: Used to Access the class attributes.
    :param menu_dict: Used to Store the menu items in a dictionary.
    :return: A dictionary with a key of recent_files and a value of the list menu_items_list.
    """
    menu_items_list = menu_dict["recent_files"]
    for menu_item in menu_items_list:
        if menu_item == RECENT_FILES_STRING:
            menu_items_list.remove(menu_item)
        if "" in menu_item:
            menu_items_list.remove("")
    return {"recent_files": menu_items_list}


def save_settings(self) -> None:
    """
    The save_settings function saves the current settings to menu.config.
    It does this by first getting the recent files items from the menu, and then
    converting that list into a dictionary using output_menu_config_as_dict().
    The function then removes any unnecessary entries from that dictionary using
    remove_unnecessary_entries(), which is also defined in this file. The final step
    is to save that new dictionary as a .conf file.

    :param self: Used to Access the class attributes.
    :return: None.
    """

    """Save settings to menu.config."""
    recent_files = menu.get_recent_files_items_menu(self)
    menu_dict = output_menu_config_as_dict(recent_files)
    new_menu_dict = remove_unnecessary_entries_from_menu_dict(self, menu_dict)
    save_menu_to_conf_file(new_menu_dict)
