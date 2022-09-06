"""settings.operations module"""

import json

from fbs_runtime.application_context.PyQt6 import ApplicationContext
from file.file import read_json_file

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
                "importNewPlaylist": components_dict["shortcut_1"],
                "exportPlaylist": components_dict["shortcut_2"],
                "clearPlaylist": components_dict["shortcut_3"],
                "generatePlaylist": components_dict["shortcut_4"],
                "shufflePlaylist": components_dict["shortcut_5"],
            }
        ],
    }
