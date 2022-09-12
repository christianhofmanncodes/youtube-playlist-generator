"""settings.operations module"""

import json

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file.file import read_json_file
from main import MainWindow
from menu import menu

app_context = ApplicationContext()


def get_settings() -> dict:
    """Return content from settings.config."""
    return read_json_file(
        app_context.get_resource("config/settings.config"),
    )


def save_settings_to_conf_file(settings_dict: dict) -> None:
    """Write content from dict to settings.config."""
    with open(
        app_context.get_resource("config/settings.config"),
        "w",
        encoding="UTF-8",
    ) as file:
        json.dump(settings_dict, file, indent=4)


def save_menu_to_conf_file(menu_dict: dict) -> None:
    """Write content from dict to menu.config."""
    with open(
        app_context.get_resource("config/menu.config"),
        "w",
        encoding="UTF-8",
    ) as file:
        json.dump(menu_dict, file, indent=4)


def output_settings_as_dict(
    components_dict: dict,
) -> dict:
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
                "removeDuplicates": components_dict["shortcut_11"],
                "copyURL": components_dict["shortcut_12"],
            }
        ],
    }


def output_menu_config_as_dict(recent_files: list) -> dict:
    """Generate dict from menu items."""
    return {"recent_files": list(recent_files)}


def load_settings(self) -> None:
    """Load settings from menu.config."""
    MainWindow.create_recent_file_menu(self)
    menu.load_recent_files(self)


def save_settings(self) -> None:
    """Save settings to menu.config."""
    menu.delete_unnecessary_entries_recent_file_menu(self)
    recent_files = menu.get_recent_files_items_menu(self)
    menu_dict = output_menu_config_as_dict(recent_files)
    save_menu_to_conf_file(menu_dict)
