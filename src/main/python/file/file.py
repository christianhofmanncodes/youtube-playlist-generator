"""file.file module"""

import json
import logging


def read_json_file(filename: str) -> dict:
    """
    The read_json_file function reads a json file and returns the content as a dictionary.
    It takes one argument, which is the filename of the json file to be read.

    :param filename:str: Used to Specify the name of the file to be read.
    :return: A dictionary.
    """
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
        return data
    except json.decoder.JSONDecodeError:
        logging.error("JSON file empty!")
        return {}
    except FileNotFoundError:
        logging.error("File %s not found!", filename)
        return {}


def read_file(filename: str) -> str:
    """
    The read_file function reads the contents of a file and returns it as a string.

    :param filename:str: Used to Specify the name of the file that is to be read.
    :return: The content from a file as a string.
    """
    with open(filename, "r", encoding="UTF-8") as file:
        file_str = file.read()
    return file_str


def write_json_file(filename: str, content: dict) -> None:
    """
    The write_json_file function writes a json file with the given filename and content.
    The function takes two arguments:
        - filename (str): The name of the file to be written.
        - content (dict): The dictionary containing
          all information to be written into the json file.

    :param filename:str: Used to Specify the name of the file that is to be written.
    :param content:dict: Used to Store the content that will be written into the json file.
    :return: None.
    """
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(content, file, indent=4)


def check_file_format(filename: str, file_format: str) -> bool:
    """
    The check_file_format function checks if the file_format is in the filename.
    It returns True if it is, and False otherwise.

    :param filename:str: Used to Specify the file name.
    :param file_format:str: Used to Check if the file_format is in the filename.
    :return: A boolean value, which is true if the file_format argument is in the filename argument.
    """
    return file_format in filename


def export_ytplaylist_file(filename: str, ytplaylist_dict: dict) -> None:
    """
    The export_ytplaylist_file function writes the playlist title
    and playlist items from a given dict to a file.
    The filename is the name of the ytplaylist file, while ytplaylist_dict
    is a dictionary containing two keys:
        'Playlist Title' and 'Playlist Items'.
    The function will write these values to an output file with extension .ytplaylist.

    :param filename:str: Used to Specify the name of the file that will be created.
    :param ytplaylist_dict:dict: Used to Pass the playlist dict to the function.
    :return: None.
    """
    write_json_file(filename=filename, content=ytplaylist_dict)
