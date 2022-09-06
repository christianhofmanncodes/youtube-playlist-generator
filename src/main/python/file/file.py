"""file.file module"""

import json


def read_json_file(filename: str) -> dict:
    """Return content from json-file."""
    with open(filename, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def read_file(filename: str) -> str:
    """Return content from file."""
    with open(filename, "r", encoding="UTF-8") as file:
        file_str = file.read()
    return file_str


def write_json_file(filename: str, content: dict) -> None:
    """Write content into json file by given filename."""
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(content, file, indent=4)
