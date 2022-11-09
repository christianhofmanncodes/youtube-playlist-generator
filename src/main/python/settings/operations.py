"""settings.operations module"""

import json

from file.file import read_json_file
from menu import menu
from settings.settings import (
    DEFAULT_SETTINGS_FILE_LOCATION,
    RECENT_FILES_STRING,
    SETTING_FILE_LOCATION,
)


def get_settings(filename: str, app_context) -> dict:
    """
    The get_settings function returns the settings.config file as a dictionary.

    :return: A dictionary.
    """
    return read_json_file(
        app_context.get_resource(filename),
    )


def get_default_settings(filename: str, app_context) -> dict:
    """
    The get_default_settings function returns the settings_default.config file as a dictionary.

    :return: A dictionary.
    """
    return read_json_file(app_context.get_resource(filename))


def save_settings_to_conf_file(settings_dict: dict, filename: str, app_context) -> None:
    """
    The save_settings_to_conf_file function writes the content
    of a dictionary to the specified filename.

    :param settings_dict:dict: Used to Pass the settings dictionary to.
    :param filename:str: Used to Pass the filename of the settings.
    :return: None.
    """
    with open(
        app_context.get_resource(filename),
        "w",
        encoding="UTF-8",
    ) as file:
        json.dump(settings_dict, file, indent=4)


def save_menu_to_conf_file(menu_dict: dict, app_context) -> None:
    """
    The save_menu_to_conf_file function writes the content of a dictionary to a file.
    The function takes one argument, menu_dict,
    which is the dictionary that will be written to file.

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

    :param components_dict:dict: Used to Pass the dictionary of settings
           from the settings dialog to this function.
    :param : Used to Generate the settings dict.
    :return: A dictionary with the settings that are inside the settings dialog.
    """
    return {
        "general": [
            {
                "openURL": components_dict["option_1"],
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

    :param recent_files:list: Used to Pass a list of recent files
           to the output_menu_config function.
    :return: A dictionary with a single key, "recent_files",
             which has a value of the recent files list.
    """
    return {"recent_files": list(recent_files)}


def load_settings(self, app, app_context) -> None:
    """
    The load_settings function loads the settings from menu.config into the program.

    :param self: Used to Access the attributes and methods of the class.
    :return: None.
    """
    menu.load_recent_files(self, app, app_context)
    menu.apply_shortcuts_to_actions(self, app_context)


def remove_unnecessary_entries_from_menu_dict(menu_dict) -> dict:
    """
    The remove_unnecessary_entries_from_menu_dict function removes
    the RECENT_FILES_STRING and empty strings from the recent files list
    in the menu dictionary. This is done to prevent these entries
    from being displayed in the menu bar.

    :param self: Used to Access the class attributes.
    :param menu_dict: Used to Store the menu items in a dictionary.
    :return: A dictionary with a key of recent_files and a value of the list menu_items_list.
    """
    menu_items_list = menu_dict["recent_files"]
    for menu_item in menu_items_list:
        if menu_item == RECENT_FILES_STRING:
            menu_items_list.remove(menu_item)
        if menu_item == " ":
            menu_items_list.remove(menu_item)
        menu_items_list = [item for item in menu_items_list if item]
    return {"recent_files": menu_items_list}


def save_settings(self, app_context) -> None:
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
    recent_files = menu.get_recent_files_items_menu(self)
    menu_dict = output_menu_config_as_dict(recent_files)
    new_menu_dict = remove_unnecessary_entries_from_menu_dict(menu_dict)
    save_menu_to_conf_file(new_menu_dict, app_context)


def check_if_settings_not_default(self, app_context) -> bool:
    """
    The check_if_settings_not_default function checks if the current settings are not default.
    It does this by comparing the current settings to the default settings.
    If they are different, then it returns True, otherwise it returns False.

    :param self: Used to Access variables that belongs to the class.
    :return: True if the current settings are not default.
    """
    current_settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)
    default_settings_dict = get_default_settings(
        DEFAULT_SETTINGS_FILE_LOCATION, app_context
    )
    return current_settings_dict != default_settings_dict


def check_if_language_was_changed(self, app_context, selected_language) -> bool:
    """
    The check_if_language_was_changed function checks if the language was changed in the settings.

    :param self: Used to Access the class attributes.
    :param app_context: Used to Access the app_context.
    :return: True if the language was changed, false otherwise.
    """
    current_settings_dict = get_settings(SETTING_FILE_LOCATION, app_context)
    return current_settings_dict["general"][0]["programLanguage"] != selected_language
